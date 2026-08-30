from fastapi import FastAPI,HTTPException
from .config import DB_PATH
from .db import fetch_all,fetch_one
from .schemas import ProductMetricsRequest,SupportRequest,CustomerHealthRequest,FeedbackSearchRequest,ExecutiveSummaryRequest

app=FastAPI(title="TaskFlow Product Intelligence API",version="1.0.0",
 description="Controlled read-only API for TaskFlow product-health data and ElevenLabs tools.")

@app.get("/health")
def health():
    return {"status":"ok","database":str(DB_PATH),"database_exists":DB_PATH.exists()}

@app.get("/api/v1/company/overview")
def company_overview():
    row=fetch_one("SELECT * FROM company_metrics LIMIT 1")
    if not row: raise HTTPException(404,"Company metrics not found")
    return {"data":row}

@app.post("/api/v1/product-metrics/query")
def product_metrics(req:ProductMetricsRequest):
    columns={"nps":"nps","monthly_active_users":"monthly_active_users","mobile_active_users":"mobile_active_users",
             "free_to_paid_conversion_pct":"free_to_paid_conversion_pct","retention_30d_pct":"retention_30d_pct",
             "avg_session_minutes":"avg_session_minutes","p95_api_latency_ms":"p95_api_latency_ms"}
    col=columns[req.metric]
    sql=f"SELECT month,{col} AS value FROM product_metrics WHERE 1=1"; p=[]
    if req.start_month: sql+=" AND month>=?"; p.append(req.start_month)
    if req.end_month: sql+=" AND month<=?"; p.append(req.end_month)
    sql+=" ORDER BY month"
    return {"metric":req.metric,"results":fetch_all(sql,tuple(p))}

@app.post("/api/v1/support/query")
def support_query(req:SupportRequest):
    sql="""SELECT month,category,priority,COUNT(*) ticket_count,
    SUM(CASE WHEN churn_risk IN ('High','Critical') THEN 1 ELSE 0 END) high_or_critical_risk_count,
    ROUND(AVG(resolution_hours),2) avg_resolution_hours
    FROM support_tickets WHERE 1=1"""
    p=[]
    for field,col,op in [("start_month","month",">="),("end_month","month","<="),("category","category","="),
                          ("priority","priority","="),("churn_risk","churn_risk","="),("account_id","account_id","=")]:
        val=getattr(req,field)
        if val is not None and val != "": sql+=f" AND {col}{op}?"; p.append(val)
    sql+=" GROUP BY month,category,priority ORDER BY month DESC,ticket_count DESC LIMIT ?"; p.append(req.limit)
    return {"filters":req.model_dump(),"results":fetch_all(sql,tuple(p))}

@app.post("/api/v1/support/monthly-trend")
def support_trend():
    rows=fetch_all("SELECT month,COUNT(*) ticket_count FROM support_tickets GROUP BY month ORDER BY month")
    for i,r in enumerate(rows):
        r["mom_change_pct"]=round((r["ticket_count"]/rows[i-1]["ticket_count"]-1)*100,2) if i else None
    return {"results":rows}

@app.post("/api/v1/support/august-summary")
def support_august_summary():
    rows=fetch_all("SELECT category, priority, ticket_count, high_or_critical_risk, avg_resolution_hours FROM support_august_summary")
    return {"results":rows}    

@app.post("/api/v1/customer-health/query")
def customer_health(req:CustomerHealthRequest):
    sql="""SELECT ah.account_id,ad.account_name,ad.segment,ad.industry,
    ah.annual_recurring_revenue,ah.tickets_last_30d,ah.latest_nps,
    ah.mobile_usage_change_pct,ah.overall_usage_change_pct,ah.churn_risk_score,ah.churn_risk
    FROM account_health ah JOIN account_dimension ad ON ad.account_id=ah.account_id WHERE 1=1"""
    p=[]
    if req.segment: sql+=" AND ad.segment=?"; p.append(req.segment)
    if req.risk_level: sql+=" AND ah.churn_risk=?"; p.append(req.risk_level)
    if req.minimum_arr is not None: sql+=" AND ah.annual_recurring_revenue>=?"; p.append(req.minimum_arr)
    sql+=" ORDER BY ah.churn_risk_score DESC,ah.annual_recurring_revenue DESC LIMIT ?"; p.append(req.limit)
    return {"filters":req.model_dump(),"results":fetch_all(sql,tuple(p))}

@app.post("/api/v1/feedback/query")
def feedback_query(req:FeedbackSearchRequest):
    sql="""SELECT feedback_id,feedback_date,account_id,customer_id,source,platform,topic,
    category,sentiment,nps_score,feedback_text FROM user_feedback WHERE 1=1"""
    p=[]
    for field,col in [("month","month"),("platform","platform"),("sentiment","sentiment"),("category","category")]:
        val=getattr(req,field)
        if val: sql+=f" AND {col}=?"; p.append(val)
    if req.query:
        sql+=" AND (feedback_text LIKE ? OR topic LIKE ? OR category LIKE ?)"
        q=f"%{req.query}%"; p += [q,q,q]
    sql+=" ORDER BY feedback_date DESC LIMIT ?"; p.append(req.limit)
    return {"filters":req.model_dump(),"results":fetch_all(sql,tuple(p))}

@app.post("/api/v1/executive/overview")
def executive_overview(req:ExecutiveSummaryRequest):
    return {"question":req.question,"facts":{
        "company":fetch_one("SELECT * FROM company_metrics LIMIT 1"),
        "current_product_metrics":fetch_one("SELECT * FROM product_metrics ORDER BY month DESC LIMIT 1"),
        "previous_product_metrics":fetch_one("SELECT * FROM product_metrics ORDER BY month DESC LIMIT 1 OFFSET 1"),
        "support_latest_months":fetch_all("SELECT month,COUNT(*) ticket_count FROM support_tickets GROUP BY month ORDER BY month DESC LIMIT 2"),
        "top_churn_risk_accounts":fetch_all("""SELECT account_id,annual_recurring_revenue,churn_risk_score,churn_risk
        FROM account_health WHERE churn_risk IN ('High','Critical')
        ORDER BY churn_risk_score DESC,annual_recurring_revenue DESC LIMIT 10""")
    }}

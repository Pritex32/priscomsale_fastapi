from fastapi import FastAPI
from routers import sales, restock,expenses, payments,inventory,employees


app = FastAPI(title="PriscomSales API")

# Include Routers
app.include_router(sales.router, prefix="/api/sales", tags=["sales"])
app.include_router(restock.router, prefix="/api/restock", tags=["restock"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])


from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": str(exc),
            "type": str(type(exc)),
            "traceback": traceback.format_exc()
        }
    )

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Route not found",
            "path": request.url.path,
            "method": request.method
        }
    )

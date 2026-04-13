import os
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application
from bot.main import register_handlers  # Importing your separate bot logic

TOKEN = "7048645118:AAEMrkg7tQvSgFFdGOT4JuzNvVNO2v_Isxk"

# Initialize PTB Application
# We don't use .run_polling() or .start() because Vercel handles the execution life
ptb_app = Application.builder().token(TOKEN).build()
register_handlers(ptb_app)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Status": "Bot is running"}

@app.post("/webhook")
async def process_update(request: Request):
    if request.method == "POST":
        data = await request.json()
        update = Update.de_json(data, ptb_app.bot)
        
        # We must initialize and shutdown the app context for each request 
        # in a serverless environment to ensure the network loop works.
        async with ptb_app:
            await ptb_app.process_update(update)
            
        return Response(status_code=200)
    return Response(status_code=405)
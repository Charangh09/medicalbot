# Interactive script to securely write real API keys to the project's .env file
# Run from PowerShell (no admin required):
# cd 'C:\Users\sirik\OneDrive\Desktop\agentaibot\agentbot' ; .\scripts\set_env.ps1

param()

Write-Host "This script will prompt you for API keys and write them to .env in the current folder." -ForegroundColor Cyan

function Read-Secret($prompt) {
    $secure = Read-Host -AsSecureString -Prompt $prompt
    if (-not $secure) { return "" }
    $ptr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) } finally { [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

$groq = Read-Secret "GROQ API Key (leave blank to keep disabled)"
$pinecone = Read-Secret "Pinecone API Key (leave blank if not using Pinecone)"
$pine_env = Read-Host -Prompt "Pinecone Environment (leave blank for default)"
$tavily = Read-Secret "Tavily API Key (leave blank to keep disabled)"
$fastapi = Read-Host -Prompt "FASTAPI_BASE_URL (default: http://localhost:8000)"

if (-not $fastapi) { $fastapi = "http://localhost:8000" }
if (-not $pine_env) { $pine_env = "" }

$envPath = Join-Path -Path (Get-Location) -ChildPath ".env"

$content = @()
$content += ('GROQ_API_KEY="' + $groq + '"')
$content += ('PINECONE_API_KEY="' + $pinecone + '"')
$content += ('PINECONE_ENVIRONMENT="' + $pine_env + '"')
$content += ('TAVILY_API_KEY="' + $tavily + '"')
$content += ('FASTAPI_BASE_URL="' + $fastapi + '"')

# Write file
Set-Content -Path $envPath -Value ($content -join "`n") -Encoding UTF8

Write-Host "Wrote .env to $envPath" -ForegroundColor Green
Write-Host "Restart your backend (uvicorn) so the new keys are picked up." -ForegroundColor Yellow

Write-Host "Example restart commands:" -ForegroundColor Cyan
Write-Host "cd 'C:\Users\sirik\OneDrive\Desktop\agentaibot\agentbot'" -ForegroundColor Gray
Write-Host ".\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Gray

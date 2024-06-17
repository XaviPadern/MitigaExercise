# Start Docker Compose
Write-Host "Starting Docker Compose services..."
docker-compose -f "..\docker-compose.yaml" up -d

# Check if Docker Compose started successfully
if ($LastExitCode -ne 0) {
    Write-Host "Failed to start Docker Compose services."
    exit $LastExitCode
}

$env:PYTHONPATH = "D:\Code\MitigaExercise"

# Run pytest
Write-Host "Running pytest..."
pytest test_integration.py

# Save the exit code of pytest
$testExitCode = $LastExitCode

# Stop Docker Compose
Write-Host "Stopping Docker Compose services..."
docker-compose down

# Exit with the pytest exit code
exit $testExitCode
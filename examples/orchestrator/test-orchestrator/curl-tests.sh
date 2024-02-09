echo "🏁  Initialize Orchestrator before Run"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"objectives": [], "modelProperties": {}, "hyperparameters": {}}' 'http://localhost:8080/v1/mistk/orchestrator/initialize'
sleep .5
echo "🧢  Register Agent 1"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/registerAgent?agentName=a&agentUrl=c'
sleep .5
echo "🧢  Register Agent 2"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/registerAgent?agentName=a&agentUrl=c'
sleep .5
echo "🚦  Start Episode"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' 'http://localhost:8080/v1/mistk/orchestrator/startEpisode'
sleep .5
echo "🛑  Stop Episode"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/stopEpisode'
sleep .5
echo "🔄  Reset"
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/reset'
sleep .5
echo "🏁  Initialize Orchestrator after Run"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' 'http://localhost:8080/v1/mistk/orchestrator/initialize'
sleep .5
echo "✅  Orchestrator Curl Tests Completed"

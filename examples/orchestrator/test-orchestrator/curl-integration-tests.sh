echo "🏁  Initialize Orchestrator before Run"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"objectives": [], "modelProperties": {}, "hyperparameters": {}}' 'http://localhost:8080/v1/mistk/orchestrator/initialize'
sleep .5
echo "🏁  Initialize Agents on Port 8081"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' -d '{"objectives": [], "modelProperties": {"low": 0, "high": 4, "size": 1}, "hyperparameters":{}}' "http://localhost:8081/v1/mistk/agent/initialize"
sleep .5
echo "📦  Build Models for Agents on Port 8081"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:8081/v1/mistk/agent/buildModel?modelPath=%2Fpath"
sleep .5
echo "🧢  Register Agents on Port 8081"
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/registerAgent?agentName=player0a&agentUrl=http%3A%2F%2Fatl-test-agent1%3A8081%2Fv1%2Fmistk%2Fagent'
sleep .5
echo "🚦  Start Episode (we'll give this 30 seconds to run)"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' 'http://localhost:8080/v1/mistk/orchestrator/startEpisode'
sleep 30
echo "🛑  Stop Episode"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/stopEpisode'
sleep .5
echo "🔄  Reset Orchestrator and Agents"
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' 'http://localhost:8080/v1/mistk/orchestrator/reset'
sleep .5
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' "http://localhost:8081/v1/mistk/agent/reset?unloadModel=false"
#sleep .5
#curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' "http://localhost:8082/v1/mistk/agent/reset?unloadModel=false"
sleep .5
echo "💾  Save Models for Agents Port 8081-8082"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:8081/v1/mistk/agent/saveModel?modelPath=."
#sleep .5
#curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:8082/v1/mistk/agent/saveModel?modelPath=."
echo "🏁  Initialize Orchestrator after Run"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' 'http://localhost:8080/v1/mistk/orchestrator/initialize'
sleep .5
echo "✅  Orchestrator + Agent Curl Tests Completed"


if [[ "$1" == "" ]]; then
    echo "🚨  ERROR: You must supply a port number to your agent in your terminal command"
    exit 1
else
    echo "🔍  We will test Agent on Port Number: $1"
fi

echo "🏁  Initialize Agent"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' -d '{"objectives": [], "modelProperties": {"learner_module": "random_sml", "learner_name": "RandomInt", "learner_kwargs": {"low": 0, "high": 4, "size": 1}, "path": ""}, "hyperparameters":{}}' "http://localhost:8081/v1/mistk/agent/initialize"
sleep .5
echo "📦  Build Model"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:8081/v1/mistk/agent/buildModel"
sleep .5
echo "💾  Save Model post Build"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:$1/v1/mistk/agent/saveModel?modelPath=."
sleep .5
echo "🏷️  Registered Agent"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' -d '{}' "http://localhost:$1/v1/mistk/agent/agentRegistered"
sleep .5
echo "💾  Save Model post Registration"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:$1/v1/mistk/agent/saveModel?modelPath=."
sleep .5
echo "✅  Episode Started"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' -d '{}' "http://localhost:$1/v1/mistk/agent/episodeStarted"
sleep .5
echo "🕹️  Get Action"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' "http://localhost:$1/v1/mistk/agent/getAction"
sleep .5
echo "💡  Replay Action"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{}' "http://localhost:$1/v1/mistk/agent/replayAction"
sleep .5
echo "🛑  Episode Stopped"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:$1/v1/mistk/agent/episodeStopped"
sleep .5
echo "🔄  Reset"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' "http://localhost:$1/v1/mistk/agent/reset?unloadModel=false"
sleep .5
echo "💾  Save Model post Run"
curl -i -X POST --header 'Content-Type: application/json' --header 'Accept: text/html' "http://localhost:$1/v1/mistk/agent/saveModel?modelPath=."
echo "✅  Agent Curl Tests Completed"

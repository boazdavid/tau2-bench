import threading
import time
import uvicorn
from uvicorn import Config, Server

from tau2 import cli
from tau2.data_model.simulation import RunConfig
from tau2.run import run_domain

def start_server():
    # port = 8001
    # config = Config("src.tau2.api_service.simulation_service:app", host="127.0.0.1", port=port, log_level="info")
    # server = Server(config)
    # # This will block until the server stops
    # server.run()
    from tau2.scripts.show_domain_doc import main as domain_main
    return domain_main(domain="telecom")

# Start the server in a thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait until the server is ready (naive method)
time.sleep(2)  # or better: probe the server until it's responsive

# Run your post-server code
print("✅ Uvicorn server should be up — now running additional logic...")

run_domain(
    RunConfig(
        domain="telecom",
        # task_set_name=args.task_set_name,
        # task_ids=args.task_ids,
        num_tasks=1,
        agent="remote_collie",
        llm_agent="azure/gpt-4o-2024-08-06",
        # llm_args_agent=args.agent_llm_args,
        # user=args.user,
        llm_user="azure/gpt-4o-2024-08-06",
        # llm_args_user=args.user_llm_args,
        num_trials=1,
        # max_steps=args.max_steps,
        # max_errors=args.max_errors,
        # save_to=args.save_to,
        max_concurrency=1,
        # seed=args.seed,
        # log_level=args.log_level,
    )
)
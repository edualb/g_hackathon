```
Traceback (most recent call last):
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/google/api_core/grpc_helpers.py", line 76, in error_remapped_callable
    return callable_(*args, **kwargs)
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/grpc/_channel.py", line 1176, in __call__
    return _end_unary_response_blocking(state, call, False, None)
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/grpc/_channel.py", line 1005, in _end_unary_response_blocking
    raise _InactiveRpcError(state)  # pytype: disable=not-instantiable
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.INTERNAL
	details = "Internal error encountered."
	debug_error_string = "UNKNOWN:Error received from peer ipv4:216.58.215.138:443 {created_time:"2024-04-03T21:33:08.094032626+01:00", grpc_status:13, grpc_message:"Internal error encountered."}"
>

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/./main.py", line 39, in <module>
    main()
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/./main.py", line 36, in main
    post()
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/./main.py", line 28, in post
    synergies = get_synergies(prompts[0])
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/gemini/gemini.py", line 84, in get_synergies
    response_scores = model.generate_content(
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/vertexai/generative_models/_generative_models.py", line 351, in generate_content
    return self._generate_content(
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/vertexai/generative_models/_generative_models.py", line 432, in _generate_content
    gapic_response = self._prediction_client.generate_content(request=request)
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/google/cloud/aiplatform_v1beta1/services/prediction_service/client.py", line 2080, in generate_content
    response = rpc(
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/google/api_core/gapic_v1/method.py", line 131, in __call__
    return wrapped_func(*args, **kwargs)
  File "/home/edualb/Documents/Workspace/ravendawn-skills-extractor/api/.venv/lib/python3.10/site-packages/google/api_core/grpc_helpers.py", line 78, in error_remapped_callable
    raise exceptions.from_grpc_error(exc) from exc
google.api_core.exceptions.InternalServerError: 500 Internal error encountered.

```
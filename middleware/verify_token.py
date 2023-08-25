import logging
import time
import traceback
from functools import wraps

from django.http import JsonResponse


def blog_verify_token_middleware(func):
    @wraps(func)
    def verify_token_handler(request, *args, **kwargs):
        timestamp = str(int(round(time.time() * 1000)))
        try:
            headers = request.headers
            verify_res = check_access_token(headers.get('token'))
            assert verify_res, {'status': 0, 'msg': '验签失败', 'data': {}, 'date': timestamp}
        except AssertionError as e:
            response_data = e.args[0]
            return JsonResponse(response_data, status=401)
        except Exception as e:
            return JsonResponse({'status': 0, 'msg': '验签失败', 'data': str(e), 'date': timestamp},
                                status=401)
        try:
            kwargs['user_info'] = verify_res
            response_data = await func(request, *args, **kwargs)
            if isinstance(response_data, dict):
                return JsonResponse(response_data)
            return response_data
        except AssertionError as e:
            response_data = e.args[0]
            return JsonResponse(response_data)
        except Exception as e:
            logging.warning(traceback.format_exc())
            response_data = {'status': -1, 'msg': '请求失败', 'data': str(e), 'date': timestamp}
            return JsonResponse(response_data)

    return verify_token_handler

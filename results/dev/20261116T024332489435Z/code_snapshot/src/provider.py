"""Bounded DeepSeek HTTP transport; logs never contain Authorization headers."""
import json
import time
import urllib.request
import urllib.error


class ProviderError(RuntimeError):
    def __init__(self, status=None):
        self.status = status
        super().__init__('Provider request failed' + (f' (HTTP {status})' if status else ''))


class DeepSeek:
    def __init__(self, settings, timeout=45, retries=2):
        if settings.get('API_ENDPOINT') != 'https://api.deepseek.com' or settings.get('API_MODEL') != 'deepseek-flash':
            raise ValueError('Provider must match the approved endpoint/model')
        if settings.get('API_THINKING') != 'disabled' or not (settings.get('API_KEY') or '').strip():
            raise ValueError('Missing key or unexpected thinking setting')
        self.key = settings['API_KEY'].strip()
        self.model = settings['API_MODEL']
        self.timeout, self.retries = timeout, retries
        self.records = []

    def complete(self, messages, tools, choice):
        payload = {'model': self.model, 'messages': messages, 'tools': tools, 'tool_choice': choice,
                   'thinking': {'type': 'disabled'}, 'max_tokens': 640, 'stream': False, 'temperature': 0}
        for attempt in range(self.retries + 1):
            start = time.perf_counter()
            record = {'attempt': attempt + 1, 'request': json.loads(json.dumps(payload))}
            self.records.append(record)
            request = urllib.request.Request('https://api.deepseek.com/chat/completions',
                data=json.dumps(payload).encode('utf-8'), headers={'Authorization': 'Bearer ' + self.key,
                'Content-Type': 'application/json', 'User-Agent': 'Day07AgentLab/1.0'})
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    data = json.load(response)
                choice_data = data['choices'][0]
                record.update(status='ok', served_model=data.get('model'), usage=data.get('usage', {}),
                              finish_reason=choice_data.get('finish_reason'), response=choice_data['message'])
                return choice_data['message']
            except urllib.error.HTTPError as exc:
                record.update(status='error', http_status=exc.code)
                try:
                    delay = float(exc.headers.get('Retry-After', min(2 ** attempt, 10)))
                except (ValueError, TypeError):
                    delay = min(2 ** attempt, 10)
                if exc.code not in (429, 500, 502, 503, 504) or attempt == self.retries or not 0 <= delay <= 10:
                    raise ProviderError(exc.code) from None
                record['retry_delay_seconds'] = delay
                time.sleep(delay)
            except (OSError, ValueError, KeyError, IndexError, TypeError):
                record.update(status='error', error='transport_or_response')
                raise ProviderError() from None
            finally:
                record['elapsed_seconds'] = time.perf_counter() - start

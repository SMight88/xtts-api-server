import wave

import riva.client
from loguru import logger


class RivaTTSInference:
    """Riva TTS inference"""

    def __init__(
            self,
            riva_port: str = '50063',
            riva_host: str = 'localhost',
            language_code: str = 'en-US',
            sample_rate: int = 24000,
            voice_name: str = 'English-US',
            nchannels: int = 1,
            sampwidth: int = 2,
            quality: int = 20,
            **kwargs
    ) -> None:
        """Riva TTS inference. Initialization"""
        self.RIVA_HOST = riva_host
        self.RIVA_PORT = riva_port
        self.RIVA_URI = self.get_uri()
        self.auth = self.get_auth()
        self.tts_service = self.get_tts_service()
        self.language_code = language_code
        self.sample_rate = sample_rate
        self.voice_name = voice_name
        self.nchannels = nchannels
        self.sampwidth = sampwidth
        self.quality = quality
        self.is_riva_tts_available = self.riva_tts_check()

    def get_uri(self) -> str:
        return f'{self.RIVA_HOST}:{self.RIVA_PORT}'

    def get_auth(self) -> riva.client.Auth:
        return riva.client.Auth(uri=self.RIVA_URI)

    def get_tts_service(self) -> riva.client.SpeechSynthesisService:
        """Get Riva client SpeechSynthesisService"""
        return riva.client.SpeechSynthesisService(self.auth)

    def riva_tts_check(self):
        try:
            self.synthesize('Test')
            logger.info('Riva TTS model available and ready.')
            return True
        except Exception as e:
            logger.error(e)
            logger.warning('Riva TTS model is not available, check Riva settings.')

    def synthesize(self, text):
        """Offline synthesize the audio by text"""
        return self.tts_service.synthesize(
            text=text,
            voice_name=self.voice_name,
            language_code=self.language_code,
            sample_rate_hz=self.sample_rate,
            quality=self.quality,
            custom_dictionary={}
        )

    def get_streaming_responses(self, text):
        return self.tts_service.synthesize_online(
            text=text,
            voice_name=self.voice_name,
            language_code=self.language_code,
            sample_rate_hz=self.sample_rate,
            quality=self.quality,
            custom_dictionary={}
        )

    def create_output_file(self, output_file):
        out_f = wave.open(output_file, 'wb')
        out_f.setnchannels(self.nchannels)
        out_f.setsampwidth(self.sampwidth)
        out_f.setframerate(self.sample_rate)
        return out_f

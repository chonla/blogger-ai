import os
import unittest
from unittest.mock import patch, MagicMock, Mock
import json

from llm.factory import use_model
from llm.openai import OpenAI
from llm.gemini import Gemini
from llm.ollama import Ollama


class LLMFactoryTests(unittest.TestCase):
    """Tests for the LLM factory use_model function"""

    def test_create_ollama_instance(self):
        """Factory should create Ollama instance for ollama:// protocol"""
        with patch.dict(os.environ, {"OLLAMA_API_BASE_URL": "http://localhost:11434"}):
            llm = use_model("ollama://llama2:13b")
            self.assertIsInstance(llm, Ollama)
            self.assertEqual(llm.model_name, "llama2:13b")

    def test_create_openai_instance(self):
        """Factory should create OpenAI instance for openai://gpt-* protocol"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            llm = use_model("openai://gpt-4")
            self.assertIsInstance(llm, OpenAI)
            self.assertEqual(llm.model_name, "gpt-4")

    def test_create_gemini_instance(self):
        """Factory should create Gemini instance for google://gemini-* protocol"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            llm = use_model("google://gemini-pro")
            self.assertIsInstance(llm, Gemini)
            self.assertEqual(llm.model_name, "gemini-pro")

    def test_invalid_namespace_raises_error(self):
        """Factory should raise ValueError for unknown namespace"""
        with self.assertRaises(ValueError):
            use_model("invalid://model-name")

    def test_malformed_url_without_protocol_raises_error(self):
        """Factory should raise ValueError for malformed URL (missing ://)"""
        with self.assertRaises(ValueError):
            use_model("ollama-model-name")

    def test_openai_without_gpt_prefix_raises_error(self):
        """Factory should raise ValueError for OpenAI model without gpt- prefix"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with self.assertRaises(ValueError):
                use_model("openai://davinci-003")

    def test_gemini_without_gemini_prefix_raises_error(self):
        """Factory should raise ValueError for Google model without gemini- prefix"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            with self.assertRaises(ValueError):
                use_model("google://some-model")

    def test_multiple_protocol_separators(self):
        """Factory should handle only first :// as separator"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            llm = use_model("openai://gpt-4://extra")
            self.assertIsInstance(llm, OpenAI)
            self.assertEqual(llm.model_name, "gpt-4://extra")


class OpenAIImplementationTests(unittest.TestCase):
    """Tests for OpenAI LLM implementation"""

    def setUp(self):
        self.system_instruction = "You are a helpful assistant."
        self.patcher = patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_openai_initialization(self):
        """OpenAI should initialize with model name"""
        llm = OpenAI("gpt-4")
        self.assertEqual(llm.model_name, "gpt-4")
        self.assertEqual(llm.history, [])

    def test_openai_with_instruction(self):
        """OpenAI should set system instruction via with_instruction method"""
        llm = OpenAI("gpt-4")
        llm.with_instruction(self.system_instruction)
        self.assertEqual(llm.system_instruction, self.system_instruction)

    def test_openai_send_message_appends_to_history(self):
        """send_message should append user message to conversation history"""
        llm = OpenAI("gpt-4")
        llm.with_instruction(self.system_instruction)
        
        # Mock the chat method
        with patch.object(llm, 'chat') as mock_chat:
            mock_chat.return_value = {
                "choices": [{"message": {"content": "Hello! How can I help?"}}]
            }
            
            response = llm.send_message("Hello")
            
            # Check message was added to history
            self.assertEqual(len(llm.history), 1)
            self.assertEqual(llm.history[0]["role"], "user")
            self.assertEqual(llm.history[0]["content"], "Hello")

    def test_openai_send_message_returns_content(self):
        """send_message should return response content"""
        llm = OpenAI("gpt-4")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            expected_response = "This is a response"
            mock_chat.return_value = {
                "choices": [{"message": {"content": expected_response}}]
            }
            
            response = llm.send_message("Hello")
            self.assertEqual(response, expected_response)

    def test_openai_clear_history(self):
        """clear_history should empty the history list"""
        llm = OpenAI("gpt-4")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            mock_chat.return_value = {
                "choices": [{"message": {"content": "Response"}}]
            }
            
            llm.send_message("Message 1")
            llm.send_message("Message 2")
            self.assertGreater(len(llm.history), 0)
            
            llm.clear_history()
            self.assertEqual(llm.history, [])

    def test_openai_initializes_without_api_key(self):
        """OpenAI can initialize without API key (raises error only on send_message)"""
        with patch.dict(os.environ, {}, clear=True):
            # Should not raise during initialization
            llm = OpenAI("gpt-4")
            self.assertEqual(llm.model_name, "gpt-4")


class GeminiImplementationTests(unittest.TestCase):
    """Tests for Gemini LLM implementation"""

    def setUp(self):
        self.system_instruction = "You are a helpful assistant."
        self.patcher = patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_gemini_initialization(self):
        """Gemini should initialize with model name"""
        llm = Gemini("gemini-pro")
        self.assertEqual(llm.model_name, "gemini-pro")
        self.assertEqual(llm.history, [])

    def test_gemini_with_instruction(self):
        """Gemini should set system instruction via with_instruction method"""
        llm = Gemini("gemini-pro")
        llm.with_instruction(self.system_instruction)
        self.assertEqual(llm.system_instruction, self.system_instruction)

    def test_gemini_send_message_appends_to_history(self):
        """send_message should append user message to conversation history with parts structure"""
        llm = Gemini("gemini-pro")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            mock_chat.return_value = {
                "candidates": [{"content": {"parts": [{"text": "Hello! How can I help?"}]}}]
            }
            
            response = llm.send_message("Hello")
            
            # Check message was added to history (Gemini uses "parts" not "content")
            self.assertEqual(len(llm.history), 1)
            self.assertEqual(llm.history[0]["role"], "user")
            self.assertEqual(llm.history[0]["parts"][0]["text"], "Hello")

    def test_gemini_send_message_returns_content(self):
        """send_message should return response content"""
        llm = Gemini("gemini-pro")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            expected_response = "This is a response"
            mock_chat.return_value = {
                "candidates": [{"content": {"parts": [{"text": expected_response}]}}]
            }
            
            response = llm.send_message("Hello")
            self.assertEqual(response, expected_response)

    def test_gemini_clear_history(self):
        """clear_history should empty the history list"""
        llm = Gemini("gemini-pro")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            mock_chat.return_value = {
                "candidates": [{"content": {"parts": [{"text": "Response"}]}}]
            }
            
            llm.send_message("Message 1")
            llm.send_message("Message 2")
            self.assertGreater(len(llm.history), 0)
            
            llm.clear_history()
            self.assertEqual(llm.history, [])

    def test_gemini_missing_api_key(self):
        """Gemini can initialize without API key (raises error only on send_message)"""
        with patch.dict(os.environ, {}, clear=True):
            # Should not raise during initialization
            llm = Gemini("gemini-pro")
            self.assertEqual(llm.model_name, "gemini-pro")


class OllamaImplementationTests(unittest.TestCase):
    """Tests for Ollama LLM implementation"""

    def setUp(self):
        self.system_instruction = "You are a helpful assistant."
        self.patcher = patch.dict(os.environ, {"OLLAMA_API_BASE_URL": "http://localhost:11434"})
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_ollama_initialization(self):
        """Ollama should initialize with model name"""
        llm = Ollama("llama2:13b")
        self.assertEqual(llm.model_name, "llama2:13b")
        self.assertEqual(llm.history, [])

    def test_ollama_with_instruction(self):
        """Ollama should set system instruction via with_instruction method"""
        llm = Ollama("llama2:13b")
        llm.with_instruction(self.system_instruction)
        self.assertEqual(llm.system_instruction, self.system_instruction)

    def test_ollama_send_message_appends_to_history(self):
        """send_message should append user message to conversation history"""
        llm = Ollama("llama2:13b")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            mock_chat.return_value = {
                "message": {"content": "Hello! How can I help?"}
            }
            
            response = llm.send_message("Hello")
            
            # Check message was added to history
            self.assertEqual(len(llm.history), 1)
            self.assertEqual(llm.history[0]["role"], "user")
            self.assertEqual(llm.history[0]["content"], "Hello")

    def test_ollama_send_message_returns_content(self):
        """send_message should return response content"""
        llm = Ollama("llama2:13b")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            expected_response = "This is a response"
            mock_chat.return_value = {
                "message": {"content": expected_response}
            }
            
            response = llm.send_message("Hello")
            self.assertEqual(response, expected_response)

    def test_ollama_strips_markdown_code_blocks(self):
        """send_message should strip markdown code blocks from responses"""
        llm = Ollama("llama2:13b")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            response_with_markdown = '```json\n{"key": "value"}\n```'
            mock_chat.return_value = {
                "message": {"content": response_with_markdown}
            }
            
            response = llm.send_message("Hello")
            self.assertNotIn("```", response)

    def test_ollama_clear_history(self):
        """clear_history should empty the history list"""
        llm = Ollama("llama2:13b")
        llm.with_instruction(self.system_instruction)
        
        with patch.object(llm, 'chat') as mock_chat:
            mock_chat.return_value = {
                "message": {"content": "Response"}
            }
            
            llm.send_message("Message 1")
            llm.send_message("Message 2")
            self.assertGreater(len(llm.history), 0)
            
            llm.clear_history()
            self.assertEqual(llm.history, [])

    def test_ollama_missing_api_base_url(self):
        """Ollama can initialize without OLLAMA_API_BASE_URL, raising error only on send_message"""
        with patch.dict(os.environ, {}, clear=True):
            # Should not raise during initialization (only when send_message calls chat)
            llm = Ollama("llama2:13b")
            self.assertEqual(llm.model_name, "llama2:13b")


class LLMBaseClassTests(unittest.TestCase):
    """Tests for base LLM class functionality"""

    def test_connection_timeout_from_environment(self):
        """LLM should respect CONNECTION_TIMEOUT_SECONDS environment variable"""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "CONNECTION_TIMEOUT_SECONDS": "25"
        }):
            llm = OpenAI("gpt-4")
            self.assertEqual(llm.connection_timeout_seconds, 25)

    def test_connection_timeout_default(self):
        """LLM should use default CONNECTION_TIMEOUT_SECONDS if not set"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True):
            llm = OpenAI("gpt-4")
            self.assertEqual(llm.connection_timeout_seconds, 15)

    def test_operation_timeout_from_environment(self):
        """LLM should respect OPERATION_TIMEOUT_SECONDS environment variable"""
        with patch.dict(os.environ, {
            "OPENAI_API_KEY": "test-key",
            "OPERATION_TIMEOUT_SECONDS": "40"
        }):
            llm = OpenAI("gpt-4")
            self.assertEqual(llm.operation_timeout_seconds, 40)

    def test_operation_timeout_default(self):
        """LLM should use default OPERATION_TIMEOUT_SECONDS if not set"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True):
            llm = OpenAI("gpt-4")
            self.assertEqual(llm.operation_timeout_seconds, 30)

    def test_logger_initialization(self):
        """LLM should initialize logger with correct namespace"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            llm = OpenAI("gpt-4")
            self.assertIsNotNone(llm.logger)
            self.assertEqual(llm.logger.namespace, "openai")

    def test_headers_include_content_type(self):
        """LLM should have Content-Type header set"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            llm = OpenAI("gpt-4")
            self.assertIn("Content-Type", llm.headers)
            self.assertEqual(llm.headers["Content-Type"], "application/json")

    def test_headers_include_authorization_for_openai(self):
        """OpenAI should have Authorization header with Bearer token"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            llm = OpenAI("gpt-4")
            self.assertIn("Authorization", llm.headers)
            self.assertEqual(llm.headers["Authorization"], "Bearer test-key")


class MultiMessageConversationTests(unittest.TestCase):
    """Tests for multi-message conversation handling"""

    def test_openai_maintains_conversation_context(self):
        """OpenAI should maintain conversation context across multiple messages"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            llm = OpenAI("gpt-4")
            llm.with_instruction("You are helpful")
            
            with patch.object(llm, 'chat') as mock_chat:
                mock_chat.return_value = {
                    "choices": [{"message": {"content": "Response"}}]
                }
                
                llm.send_message("Message 1")
                llm.send_message("Message 2")
                
                # Should have 2 messages in history
                self.assertEqual(len(llm.history), 2)
                self.assertEqual(llm.history[0]["content"], "Message 1")
                self.assertEqual(llm.history[1]["content"], "Message 2")

    def test_ollama_maintains_conversation_context(self):
        """Ollama should maintain conversation context across multiple messages"""
        with patch.dict(os.environ, {"OLLAMA_API_BASE_URL": "http://localhost:11434"}):
            llm = Ollama("llama2:13b")
            llm.with_instruction("You are helpful")
            
            with patch.object(llm, 'chat') as mock_chat:
                mock_chat.return_value = {
                    "message": {"content": "Response"}
                }
                
                llm.send_message("Message 1")
                llm.send_message("Message 2")
                
                # Should have 2 messages in history
                self.assertEqual(len(llm.history), 2)
                self.assertEqual(llm.history[0]["content"], "Message 1")
                self.assertEqual(llm.history[1]["content"], "Message 2")

    def test_gemini_maintains_conversation_context(self):
        """Gemini should maintain conversation context across multiple messages"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}):
            llm = Gemini("gemini-pro")
            llm.with_instruction("You are helpful")
            
            with patch.object(llm, 'chat') as mock_chat:
                mock_chat.return_value = {
                    "candidates": [{"content": {"parts": [{"text": "Response"}]}}]
                }
                
                llm.send_message("Message 1")
                llm.send_message("Message 2")
                
                # Should have 2 messages in history
                self.assertEqual(len(llm.history), 2)
                self.assertEqual(llm.history[0]["parts"][0]["text"], "Message 1")
                self.assertEqual(llm.history[1]["parts"][0]["text"], "Message 2")


if __name__ == '__main__':
    unittest.main()

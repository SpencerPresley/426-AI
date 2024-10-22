# ChainBuilder Module Documentation  

This module provides a set of classes to build, wrap, compose, and manage chains for language model interactions. It is designed to facilitate the creation of complex language model workflows by chaining together prompts, models, and parsers with optional preprocessing and postprocessing steps.  

**Classes:**

- `ChainBuilder`
- `ChainWrapper`
- `ChainComposer`
- `ChainManager`

---

## ChainBuilder

### Overview

The `ChainBuilder` class is responsible for constructing a runnable chain by combining a chat prompt, a language model (LLM), and an optional output parser. It encapsulates the logic required to build a chain that can be invoked with input data to generate outputs from the LLM.

### Constructor

```python
def __init__(
    self,
    *,
    chat_prompt: ChatPromptTemplate,
    llm: Union[ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI],
    parser: Optional[Union[PydanticOutputParser, JsonOutputParser]] = None,
):
```

#### Parameters

- **chat_prompt** (`ChatPromptTemplate`): The chat prompt template that defines the conversation structure between the user and the assistant.
- **llm** (`Union[ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI]`): The language model used to generate responses. Supported models include OpenAI's GPT models, Anthropic's Claude models, and Google's Generative AI models.
- **parser** (`Optional[Union[PydanticOutputParser, JsonOutputParser]]`, optional): An optional parser used to process the output from the LLM. It can be a `PydanticOutputParser` for structured Pydantic models or a `JsonOutputParser` for JSON outputs.  

### Public Methods

#### `get_chain`

```python
def get_chain(self) -> Runnable:
```

Returns the constructed chain as a `Runnable` object. This chain can be invoked with input data to generate outputs.

#### Returns

- **chain** (`Runnable`): The constructed runnable chain.

### Usage Example

```python
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    PromptTemplate,
)
from langchain.schema.runnable import Runnable
from langchain_openai import ChatOpenAI

# Define the system and human prompts
system_prompt_template = PromptTemplate(template="You are a helpful assistant.")
human_prompt_template = PromptTemplate(template="Translate '{text}' to Spanish.")

# Create message prompt templates
system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template.template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template.template)

# Create a chat prompt template
chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# Initialize the language model
llm = ChatOpenAI(model='gpt-3.5-turbo', api_key='your-api-key')

# Initialize the ChainBuilder
chain_builder = ChainBuilder(chat_prompt=chat_prompt_template, llm=llm)

# Get the runnable chain
chain = chain_builder.get_chain()

# Invoke the chain with input data
output = chain.invoke({'text': 'Hello, world!'})

print(output)  # Output should be the translation of 'Hello, world!' to Spanish.
```

### Private Methods

#### `_build_chain`

```python
def _build_chain(self) -> Runnable:
```

Constructs the chain by combining the prompt, LLM, and parser. This method is called internally during initialization.

---

## ChainWrapper

### Overview

The `ChainWrapper` class wraps a runnable chain and provides additional functionality, such as preprocessing input data, postprocessing outputs, and handling return types. It manages the chain's execution and output handling, making it easier to integrate into larger workflows.

### Constructor

```python
def __init__(
    self,
    *,
    chain: Runnable,
    parser: Optional[Union[PydanticOutputParser, JsonOutputParser]] = None,
    return_type: Optional[Literal["pydantic_model", "json"]] = None,
    preprocessor: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    postprocessor: Optional[Callable[[Any], Any]] = None,
):
```

#### Parameters

- **chain** (`Runnable`): The runnable chain to wrap.
- **parser** (`Optional[Union[PydanticOutputParser, JsonOutputParser]]`, optional): An optional parser used to process the output of the chain.
- **return_type** (`Optional[Literal["pydantic_model", "json"]]`, optional): Specifies the type of the output when this chain is the last in the sequence. Can be `'pydantic_model'` or `'json'`.
- **preprocessor** (`Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]`, optional): An optional function to preprocess the input data before invoking the chain.
- **postprocessor** (`Optional[Callable[[Any], Any]]`, optional): An optional function to postprocess the output after invoking the chain.

### Public Methods

#### `run_chain`

```python
def run_chain(
    self, 
    *, 
    input_data: Dict[str, Any] = None, 
    is_last_chain: bool = False, 
    return_type: Optional[Literal["pydantic_model", "json"]] = None
) -> Any:
```

Executes the chain with the provided input data, applying any preprocessing and postprocessing functions. Handles the output based on whether it's the last chain in a sequence and the specified return type.

#### Parameters

- **input_data** (`Dict[str, Any]`, optional): The input data to pass to the chain. Defaults to an empty dictionary if not provided.
- **is_last_chain** (`bool`, optional): Indicates whether this chain is the last in a sequence. Defaults to `False`.
- **return_type** (`Optional[Literal["pydantic_model", "json"]]`, optional): Overrides the return type specified in the constructor. Can be useful when the return type might change dynamically.

#### Returns

- **output** (`Any`): The processed output from the chain, which can be a Pydantic model, a dictionary, or a string, depending on the return type.

#### `get_parser_type`

```python
def get_parser_type(self) -> Union[str, None]:
```

Returns the type of the parser used in the chain, if any.

#### Returns

- **parser_type** (`Union[str, None]`): The name of the parser class or `None` if no parser is used.

#### `get_return_type`

```python
def get_return_type(self) -> Union[str, None]:
```

Returns the return type specified for the chain.

#### Returns

- **return_type** (`Union[str, None]`): The return type specified during initialization or `None` if not set.

### Usage Example

```python
from chain_builder import ChainWrapper
from langchain.schema.runnable import Runnable

# Assume 'chain' is a Runnable obtained from ChainBuilder
chain_wrapper = ChainWrapper(
    chain=chain,
    return_type='json',
    preprocessor=lambda x: {"text": x["text"].upper()},
    postprocessor=lambda x: x.lower(),
)

# Run the chain with input data
output = chain_wrapper.run_chain(input_data={'text': 'Hello, world!'}, is_last_chain=True)

print(output)  # Processed output from the chain
```

---

## ChainComposer

### Overview

The `ChainComposer` class allows you to compose multiple chains into a sequence, managing the flow of data between them. Each chain in the sequence can optionally pass its output to the next chain by specifying an output key name.

### Constructor

```python
def __init__(self):
```

Initializes a new `ChainComposer` instance with an empty chain sequence.

### Public Methods

#### `add_chain`

```python
def add_chain(
    self, 
    *, 
    chain_wrapper: ChainWrapper, 
    output_passthrough_key_name: Optional[str] = None
):
```

Adds a `ChainWrapper` to the chain sequence. Optionally specifies a key name under which to store the chain's output for use in subsequent chains.

#### Parameters

- **chain_wrapper** (`ChainWrapper`): The chain to add to the sequence.
- **output_passthrough_key_name** (`Optional[str]`, optional): The key name to store the chain's output in the variables dictionary.

#### `run`

```python
def run(
    self, 
    *, 
    variables: Dict[str, Any], 
    return_type: Optional[Literal["pydantic_model", "json"]] = None
) -> str:
```

Executes the chain sequence with the provided variables, passing data between chains as specified.

#### Parameters

- **variables** (`Dict[str, Any]`): The input variables required by the chains.
- **return_type** (`Optional[Literal["pydantic_model", "json"]]`, optional): Specifies the return type for the final output.

#### Returns

- **output** (`str`): The output from the final chain, serialized to a JSON-formatted string.

### Usage Example

```python
from chain_builder import ChainComposer, ChainWrapper

# Assume 'chain_wrapper1' and 'chain_wrapper2' are ChainWrapper instances
chain_composer = ChainComposer()
chain_composer.add_chain(chain_wrapper=chain_wrapper1, output_passthrough_key_name='first_output')
chain_composer.add_chain(chain_wrapper=chain_wrapper2, output_passthrough_key_name='second_output')

# Run the composed chains
final_output = chain_composer.run(variables={'initial_input': 'Start here'})

print(final_output)  # Output from the final chain in the sequence
```

---

## ChainManager

### Overview

The `ChainManager` class serves as a high-level interface for managing and executing sequences of chains. It initializes the language model, manages global variables, and provides methods for adding chain layers and running the entire sequence.

### Constructor

```python
def __init__(
    self,
    llm_model: str,
    api_key: str,
    llm_temperature: float = 0.7,
    preprocessor: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    postprocessor: Optional[Callable[[Any], Any]] = None,
    **llm_kwargs: Dict[str, Any],
):
```

#### Parameters

- **llm_model** (`str`): The name of the language model to use (e.g., `'gpt-4o-mini'`, `'claude-sonnet-3.5'`, `'gemini-pro-1.5'`)
- **api_key** (`str`): The API key for accessing the LLM service.
- **llm_temperature** (`float`, optional): The temperature setting for the LLM, controlling the randomness of outputs. Defaults to `0.7`.
- **preprocessor** (`Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]`, optional): A function to preprocess input variables before they are passed to the chains.
- **postprocessor** (`Optional[Callable[[Any], Any]]]`, optional): A function to postprocess the outputs from the chains.
- **llm_kwargs** (`Dict[str, Any]`, optional): Additional keyword arguments to pass to the LLM initialization.

### Public Methods

#### `add_chain_layer`

```python
def add_chain_layer(
    self,
    *,
    system_prompt: str,
    human_prompt: str,
    output_passthrough_key_name: Optional[str] = None,
    ignore_output_passthrough_key_name_error: bool = False,
    preprocessor: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    postprocessor: Optional[Callable[[Any], Any]]] = None,
    parser_type: Optional[Literal["pydantic", "json"]] = None,
    return_type: Optional[Literal["pydantic_model", "json"]] = None,
    pydantic_output_model: Optional[BaseModel] = None,
) -> None:
```

Adds a new chain layer to the sequence with the specified prompts and configurations.

#### Parameters

- **system_prompt** (`str`): The system prompt template for the chain.
- **human_prompt** (`str`): The human prompt template for the chain.
- **output_passthrough_key_name** (`Optional[str]`, optional): The key name to store the chain's output for use in subsequent chains.
- **ignore_output_passthrough_key_name_error** (`bool`, optional): If `True`, ignores the error when `output_passthrough_key_name` is not provided for intermediate chain layers, useful for the final chain in the sequence. Defaults to `False`.
- **preprocessor** (`Optional[Callable[[Dict[str, Any]], Dict[str, Any]]]`, optional): A function to preprocess input data for this layer.
- **postprocessor** (`Optional[Callable[[Any], Any]]]`, optional): A function to postprocess the output from this layer.
- **parser_type** (`Optional[Literal["pydantic", "json"]]`, optional): Specifies the type of parser to use. Can be `'pydantic'` or `'json'`.
- **return_type** (`Optional[Literal["pydantic_model", "json"]]`, optional): Specifies the output type when this chain is the last in the sequence.
- **pydantic_output_model** (`Optional[BaseModel]`, optional): A Pydantic model to parse the output when using a `PydanticOutputParser`.

#### Raises

- **ValueError**: If validation checks fail due to missing or invalid parameters.
- 
#### `set_global_variables`

```python
def set_global_variables(self, variables: Dict[str, Any]) -> None:
```

Sets global variables that are available to all chain layers.

#### Parameters

- **variables** (`Dict[str, Any]`): A dictionary of variables to set as global variables.
- 
#### `get_chain_sequence`

```python
def get_chain_sequence(self) -> List[Tuple[ChainWrapper, Optional[str]]]:
```

Returns the current sequence of chains as a list of tuples containing `ChainWrapper` instances and their output key names.

#### Returns

- **chain_sequence** (`List[Tuple[ChainWrapper, Optional[str]]]`): The sequence of chains.

#### `print_chain_sequence`

```python
def print_chain_sequence(self) -> None:
```

Prints the formatted chain sequence, including details about each chain layer.

#### `run`

```python
def run(self, prompt_variables_dict: Dict[str, Any]) -> str:
```

Executes the chain sequence with the provided prompt variables.

#### Parameters

- **prompt_variables_dict** (`Dict[str, Any]`): A dictionary of input variables required by the chain prompts.

#### Returns

- **output** (`str` or `BaseModel`): The output from the final chain, serialized as a JSON-formatted string or a Pydantic model, depending on the return type.

#### Raises

- **TypeError**: If `prompt_variables_dict` is not a dictionary.
- **ValueError**: If no chain layers have been added or if required configurations are missing.

### Usage Example

```python
from chain_builder import ChainManager
from pydantic import BaseModel, Field

# Define a Pydantic model for the output
class TranslationOutput(BaseModel):
    translation: str = Field(..., description="The translated text.")

# Initialize the ChainManager
chain_manager = ChainManager(
    llm_model='gpt-4o-mini',
    api_key='your-api-key',
    llm_temperature=0.5,
)

# Add a chain layer with a parser
chain_manager.add_chain_layer(
    system_prompt="You are a translation assistant.",
    human_prompt="Translate '{text}' to French.",
    output_passthrough_key_name='translation_output',
    parser_type='pydantic',
    return_type='pydantic_model',
    pydantic_output_model=TranslationOutput,
)

# Run the chain with input variables
output = chain_manager.run({'text': 'Hello, world!'})

# Access the parsed output
if isinstance(output, TranslationOutput):
    print(output.translation)  # Should print the translated text
else:
    print(output)  # If output is not a Pydantic model, print it directly
```

---

## Additional Notes

- **Error Handling:** The module includes comprehensive error handling, raising descriptive exceptions when invalid parameters are provided or when required configurations are missing.
- **Logging:** Uses Python's `logging` module to log informational messages and warnings, aiding in debugging and monitoring.
- **Extensibility:** The classes are designed to be extensible, allowing users to customize preprocessing, postprocessing, and output parsing to fit their specific needs.
- **Multi-Model Support:** Supports integration with different language models, making it flexible for various applications.

---

## Summary

The `ChainBuilder` module provides a powerful and flexible way to construct and manage complex chains of language model interactions. By abstracting the complexities of prompt management, parser integration, and data flow between chains, it allows developers to focus on building effective conversational workflows.

Whether you're building a simple translation tool or a multi-step assistant with complex logic, the classes provided in this module can help streamline the development process.

---

**Note:** Replace `'your-api-key'` with your actual API key when using the examples.
****
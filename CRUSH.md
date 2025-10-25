# Tarot App - CRUSH Configuration

## Commands

### Running Python scripts
- **Run basic tarot reader**: `python tarot_reader.py`
- **Run enhanced tarot reader**: `python tarot_reader_enhanced.py` 
- **Run quantum random generator**: `python tarot_quantum_random.py`
- **Run randomness tests**: `python tarot_randomness_test.py`

### Testing
- **Syntax check**: `python -c "import py_compile; py_compile.compile('filename.py')"`
- **Run single test**: Run individual scripts to verify functionality
- **Test randomness quality**: Use `tarot_randomness_test.py` for comprehensive testing

### Linting/Formatting
- No specific linting tools configured - check syntax with Python compile

## Code Style Guidelines

### Imports
- Standard library imports first, third-party second, local imports last
- Use absolute imports
- Group related imports together

### Naming Conventions
- **Classes**: PascalCase (e.g., `MazoTarot`, `LectorTarot`)
- **Functions/methods**: snake_case (e.g., `realizar_lectura`, `obtener_numero`)
- **Variables**: snake_case (e.g., `carta_nombre`, `tipo_tirada`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `FUENTE_ALEATORIEDAD`)
- **Enums**: PascalCase for class, UPPER_SNAKE_CASE for values

### Types
- Use type hints with `typing` module (`Dict`, `List`, `Optional`, `Tuple`)
- Use `@dataclass` for data containers
- Use `Enum` for constants and options

### Formatting
- Spanish language for user-facing strings and comments
- Docstrings in Spanish with triple quotes
- 4 spaces for indentation
- Maximum line length flexible but keep readable

### Error Handling  
- Use descriptive error messages in Spanish
- Prefer explicit error handling over silent failures
- Use appropriate exception types

### File Structure
- Each script is self-contained and executable
- Main functionality in classes, execution logic in `if __name__ == "__main__"`
- Web interface separate (HTML/JS)
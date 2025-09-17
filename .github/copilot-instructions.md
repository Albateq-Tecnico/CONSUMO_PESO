# Copilot Instructions for PREDICCION_PESO

## Project Overview
This project appears to focus on data analysis and prediction related to weight, using CSV files for input and output. The main data sources are located in the `COEFICIENTES/` directory.

## Directory Structure
- `COEFICIENTES/`: Contains CSV files with results and coefficients, such as `resultados_cons_vs_peso.csv` and `resultados_dia_vs_cons.csv`.

## Key Patterns and Conventions
- Data is stored and exchanged primarily in CSV format.
- File naming follows a pattern: `resultados_<metric>_vs_<metric>.csv`.
- All project data and results are organized under the `COEFICIENTES/` directory.

## Developer Workflows
- There are no build scripts, test files, or obvious automation tools present. Data analysis is likely performed via scripts or notebooks (not present in the current snapshot).
- To extend or analyze data, add new CSVs to `COEFICIENTES/` following the established naming convention.

## Integration Points
- No external dependencies or integrations are visible in the current codebase snapshot.

## Recommendations for AI Agents
- When generating new analysis scripts, place them at the project root or in a new `scripts/` directory.
- Maintain the CSV naming convention for consistency.
- Reference the `COEFICIENTES/` directory for all data input/output operations.
- If adding new data sources or result types, document them in this file for future contributors.

## Example
- To add a new analysis comparing "altura" (height) vs "peso" (weight), create a file named `resultados_altura_vs_peso.csv` in `COEFICIENTES/`.

---
If you add new workflows, scripts, or conventions, update this file to keep instructions current.

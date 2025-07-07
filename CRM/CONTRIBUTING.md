# Contributing

Thank you for considering a contribution.

1. Fork the repository and create a feature branch.
2. Run `pip install -r backend/requirements.txt` and `npm install`.
3. Execute `pytest` and `npm test` to ensure all tests pass.
4. Format and lint the Python code using `autoflake`, `isort`, `black` and `pylint`:
   ```bash
   autoflake --remove-all-unused-imports -r backend/
   isort backend/
   black backend/
   pylint --rcfile=.pylintrc backend/
   ```
5. Document your change in `CHANGELOG.md` under **Unreleased**.
6. Open a Pull Request on GitHub.

All code is validated against the OTAP guidelines and must include tests.

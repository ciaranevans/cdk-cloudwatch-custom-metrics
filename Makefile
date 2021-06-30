.PHONY: install
install:
	npm install
	poetry install

.PHONY: lint
lint:
	poetry run flake8 cdk/
	poetry run isort --check-only --profile black cdk/
	poetry run black --check --diff cdk/

.PHONY: format
format:
	poetry run isort --profile black cdk/
	poetry run black cdk/

.PHONY: diff
diff:
	poetry run dotenv run npx cdk diff --app cdk/app.py || true

.PHONY: deploy
deploy:
	poetry run dotenv run npx cdk deploy --app cdk/app.py --require-approval never

.PHONY: destroy
destroy:
	poetry run dotenv run npx cdk destroy --app cdk/app.py --force

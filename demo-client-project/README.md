# Demo Client Project

This is a simple demo project that demonstrates how to integrate the i18n-checker tool into a CI/CD pipeline.

## Setup

1. Install dependencies:
```
pip install i18n-checker
```

2. Add translation files to the `locales` directory

3. Run i18n validation:
```
i18n-checker --scan . --format html --output i18n_report.html
```

## CI/CD Integration

This project includes a CI/CD pipeline configuration that automatically checks for missing or unused internationalization keys. 
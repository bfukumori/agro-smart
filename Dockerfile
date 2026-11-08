# Dockerfile endurecido (Security-Hardened)
FROM python:3.12-alpine

# Metadados do Container
LABEL maintainer="AgroSmart Engineering Team"
LABEL version="1.0.0"
LABEL description="AgroSmart Autonomous IoT Telemetry, Process Mining & Decision Platform"

# Boas práticas de segurança: criar usuário não-root dedicado
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Instalar dependências necessárias para geração de gráficos no pipeline se necessário
RUN apk add --no-cache curl wget freetype libpng libjpeg-turbo

COPY . .

# Executar pipeline inicial gerando datasets e relatórios de processo
RUN python src/run_all.py

# Ajustar permissões para o usuário restrito
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8080

# Healthcheck embutido na imagem
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://127.0.0.1:8080/ || exit 1

CMD ["python", "-m", "http.server", "8080", "--directory", "dashboard"]

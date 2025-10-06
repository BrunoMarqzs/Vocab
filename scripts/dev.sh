#!/bin/bash

# Script de utilidade para o projeto Vocab
# Uso: ./scripts/dev.sh [comando]

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/src/backend"
FRONTEND_DIR="$PROJECT_ROOT/src/frontend"

case "$1" in
  "setup")
    echo "🚀 Configurando projeto Vocab..."
    
    # Setup backend
    echo "📦 Instalando dependências do backend..."
    cd "$BACKEND_DIR"
    pip install -r requirements.txt
    
    # Setup frontend
    echo "📦 Instalando dependências do frontend..."
    cd "$FRONTEND_DIR"
    npm install
    
    echo "✅ Setup concluído!"
    ;;
    
  "dev")
    echo "🔧 Iniciando modo desenvolvimento..."
    echo "Backend: http://localhost:8000"
    echo "Frontend: http://localhost:3000"
    echo ""
    
    # Iniciar backend em background
    cd "$BACKEND_DIR/app"
    uvicorn api:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    # Aguardar um pouco para o backend iniciar
    sleep 3
    
    # Iniciar frontend
    cd "$FRONTEND_DIR"
    npm run dev
    
    # Cleanup: matar processo do backend quando script terminar
    trap "kill $BACKEND_PID 2>/dev/null || true" EXIT
    ;;
    
  "test")
    echo "🧪 Executando testes..."
    cd "$BACKEND_DIR"
    PYTHONPATH="$PROJECT_ROOT/src" python -m pytest tests/ -v
    ;;
    
  "build")
    echo "🏗️ Construindo aplicação..."
    cd "$FRONTEND_DIR"
    npm run build
    echo "✅ Build concluído em src/frontend/dist/"
    ;;
    
  "docker-dev")
    echo "🐳 Iniciando com Docker (desenvolvimento)..."
    cd "$PROJECT_ROOT"
    docker-compose up backend frontend-dev
    ;;
    
  "docker-prod")
    echo "🐳 Iniciando com Docker (produção)..."
    cd "$PROJECT_ROOT"
    docker-compose up backend frontend-prod
    ;;
    
  "clean")
    echo "🧹 Limpando arquivos temporários..."
    
    # Limpar backend
    find "$PROJECT_ROOT" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -name "*.pyc" -delete 2>/dev/null || true
    
    # Limpar frontend
    rm -rf "$FRONTEND_DIR/node_modules" 2>/dev/null || true
    rm -rf "$FRONTEND_DIR/dist" 2>/dev/null || true
    rm -rf "$FRONTEND_DIR/.cache" 2>/dev/null || true
    
    echo "✅ Limpeza concluída!"
    ;;
    
  *)
    echo "Vocab - Script de Desenvolvimento"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  setup      - Instalar dependências"
    echo "  dev        - Modo desenvolvimento (backend + frontend)"
    echo "  test       - Executar testes"
    echo "  build      - Build de produção do frontend"
    echo "  docker-dev - Docker modo desenvolvimento"
    echo "  docker-prod- Docker modo produção"
    echo "  clean      - Limpar arquivos temporários"
    echo ""
    echo "Exemplos:"
    echo "  $0 setup"
    echo "  $0 dev"
    echo "  $0 test"
    ;;
esac

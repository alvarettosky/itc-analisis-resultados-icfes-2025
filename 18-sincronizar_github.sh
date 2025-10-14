#!/bin/bash

# Script para sincronizar el proyecto con GitHub
# Uso: ./sincronizar_github.sh "mensaje del commit"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║   🔄  SINCRONIZACIÓN CON GITHUB - RESULTADOS ICFES  🔄       ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar si hay cambios
echo -e "${YELLOW}📊 Verificando cambios...${NC}"
git status

# Verificar si hay archivos modificados
if [[ -z $(git status -s) ]]; then
    echo -e "${GREEN}✅ No hay cambios para sincronizar${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}📝 Archivos modificados:${NC}"
git status -s

echo ""
echo -e "${YELLOW}¿Deseas continuar con la sincronización? (s/n)${NC}"
read -r respuesta

if [[ "$respuesta" != "s" && "$respuesta" != "S" ]]; then
    echo -e "${RED}❌ Sincronización cancelada${NC}"
    exit 0
fi

# Agregar todos los archivos
echo ""
echo -e "${BLUE}📦 Agregando archivos...${NC}"
git add .

# Verificar si se proporcionó un mensaje de commit
if [ -z "$1" ]; then
    echo -e "${YELLOW}💬 Ingresa el mensaje del commit:${NC}"
    read -r mensaje
else
    mensaje="$1"
fi

# Hacer commit
echo ""
echo -e "${BLUE}💾 Creando commit...${NC}"
git commit -m "$mensaje"

# Hacer push
echo ""
echo -e "${BLUE}🚀 Subiendo cambios a GitHub...${NC}"
git push origin main

# Verificar si el push fue exitoso
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                               ║${NC}"
    echo -e "${GREEN}║   ✅  SINCRONIZACIÓN EXITOSA  ✅                             ║${NC}"
    echo -e "${GREEN}║                                                               ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}🌐 Ver en GitHub: https://github.com/alvaretto/resultados-icfes${NC}"
else
    echo ""
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                               ║${NC}"
    echo -e "${RED}║   ❌  ERROR EN LA SINCRONIZACIÓN  ❌                         ║${NC}"
    echo -e "${RED}║                                                               ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${RED}Por favor, revisa los errores arriba${NC}"
    exit 1
fi


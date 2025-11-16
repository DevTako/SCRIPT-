import asyncio
import json
import os
from telethon import TelegramClient, functions, types
from datetime import datetime
import getpass

class GrupoEmaBot:
    def __init__(self):
        # === CONFIGURA AQUÍ TUS CREDENCIALES ===
        self.api_id = 35071251  # ⚠️ REEMPLAZA con tu API ID real
        self.api_hash = 'b5b83f7452d1b89159248d4e1d4e0177'  # ⚠️ REEMPLAZA con tu API Hash real
        self.phone_number = '+584121053689'  # ⚠️ REEMPLAZA con tu número real
        # ======================================
        
        self.session_name = 'session_grupos'
        
        # Configuración de grupos
        self.config_file = 'config_grupos.json'
        self.grupos_por_lote = 50  # Grupos a crear (pocos para prueba)
        self.delay_entre_grupos = 10  # Segundos entre creación
        
        # Inicializar cliente
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        
    async def iniciar_sesion(self):
        """Inicia sesión automáticamente"""
        try:
            print(">> Iniciando sesión en Telegram...")
            
            # Intentar iniciar con sesión existente primero
            await self.client.start(phone=self.phone_number)
            
            print(">> ✅ Sesión iniciada correctamente")
            return True
            
        except Exception as e:
            print(f">> ❌ Error en inicio de sesión: {e}")
            return False
        
    def cargar_configuracion(self):
        """Carga la configuración desde archivo JSON"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Configuración por defecto
            config = {
                'ultimo_numero': 0,
                'total_grupos_creados': 0,
                'historial_grupos': []
            }
            self.guardar_configuracion(config)
            return config
    
    def guardar_configuracion(self, config):
        """Guarda la configuración en archivo JSON"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    async def crear_grupo(self, numero_grupo, config):
        """Crea un grupo individual"""
        try:
            nombre_grupo = f"{numero_grupo} ema"
            
            print(f">> Creando grupo: {nombre_grupo}")
            
            # Crear el grupo
            result = await self.client(functions.channels.CreateChannelRequest(
                title=nombre_grupo,
                about=f"Grupo EMA #{numero_grupo}",
                megagroup=True
            ))
            
            # Obtener información del grupo creado
            channel = result.chats[0]
            
            # Registrar en historial
            grupo_info = {
                'numero': numero_grupo,
                'nombre': nombre_grupo,
                'id': channel.id,
                'fecha_creacion': datetime.now().isoformat()
            }
            
            config['historial_grupos'].append(grupo_info)
            config['ultimo_numero'] = numero_grupo
            config['total_grupos_creados'] += 1
            
            print(f">> ✅ Grupo creado: {nombre_grupo} (ID: {channel.id})")
            return True
            
        except Exception as e:
            print(f">> ❌ Error creando grupo {numero_grupo}: {str(e)}")
            return False
    
    async def crear_lote_grupos(self):
        """Crea un lote de grupos automáticamente"""
        print(">> 🚀 INICIANDO CREACIÓN DE GRUPOS EMA...")
        
        # Cargar configuración
        config = self.cargar_configuracion()
        ultimo_numero = config['ultimo_numero']
        
        print(f">> Último número creado: {ultimo_numero}")
        print(f">> Creando {self.grupos_por_lote} nuevos grupos...")
        
        # Crear grupos
        grupos_creados = 0
        for i in range(1, self.grupos_por_lote + 1):
            numero_grupo = ultimo_numero + i
            
            if await self.crear_grupo(numero_grupo, config):
                grupos_creados += 1
            
            # Esperar entre grupos
            if i < self.grupos_por_lote:
                print(f">> ⏳ Esperando {self.delay_entre_grupos} segundos...")
                await asyncio.sleep(self.delay_entre_grupos)
        
        # Guardar configuración actualizada
        self.guardar_configuracion(config)
        
        print(f"\n>> 🎉 PROCESO COMPLETADO!")
        print(f">> Grupos creados en esta sesión: {grupos_creados}")
        print(f">> Total de grupos creados: {config['total_grupos_creados']}")
        print(f">> Siguiente número: {config['ultimo_numero'] + 1}")
    
    async def mostrar_estadisticas(self):
        """Muestra estadísticas de los grupos creados"""
        config = self.cargar_configuracion()
        
        print("\n>> 📊 ESTADÍSTICAS GRUPOS EMA")
        print(f">> Último número creado: {config['ultimo_numero']}")
        print(f">> Total de grupos creados: {config['total_grupos_creados']}")
        
        if config['historial_grupos']:
            print(f">> Últimos 3 grupos creados:")
            for grupo in config['historial_grupos'][-3:]:
                print(f"   #{grupo['numero']} - {grupo['nombre']}")

async def main():
    print("========================================")
    print("    BOT CREADOR DE GRUPOS EMA - FIXED")
    print("========================================")
    print(">> Modo: Automático (sin inputs)")
    print(">> Grupos por lote: 2")
    print(">> Delay entre grupos: 5 segundos")
    print("========================================\n")
    
    # Crear instancia del bot
    bot = GrupoEmaBot()
    
    # Iniciar sesión
    if await bot.iniciar_sesion():
        # Mostrar estadísticas actuales
        await bot.mostrar_estadisticas()
        
        # Crear grupos automáticamente
        await bot.crear_lote_grupos()
        
        # Mostrar estadísticas finales
        await bot.mostrar_estadisticas()
    else:
        print(">> ❌ No se pudo iniciar sesión. Verifica tus credenciales.")
    
    # Cerrar cliente
    await bot.client.disconnect()
    print(">> 👋 Sesión finalizada")

if __name__ == "__main__":
    # Ejecutar automáticamente
    asyncio.run(main())
import time
import pymem
import pymem.process
import keyboard

dwEntityList = (0x4DA2F24)
dwGlowObjectManager = (0x52EB518)
m_iGlowIndex = (0xA438)
m_iTeamNum = (0xF4)
m_flFlashMaxAlpha = (0xA41C)
dwLocalPlayer = (0xD8B2DC)
m_fFlags = (0x104)
dwForceJump = (0x524CE84)
m_bSpotted = (0x93D)
m_iDefaultFOV = (0x332C)

# don't know if this works but :shrug:
antivac = "f4we03qlwp5q3q45q5890wu4892h59ut)ZQ$/Z§W784zw0682732z57890Z/Z/(§$%Z=!""§(%/08($12\n"
print( antivac )

def main():
    print("Cobalt has launched.")
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        local_player = pm.read_int(client + dwLocalPlayer)

        if local_player:
            local_flash_alpha = (local_player + m_flFlashMaxAlpha)
            pm.write_int(local_flash_alpha, 0)
            
            local_fov = (local_player + m_iDefaultFOV)
            pm.write_int(local_fov, 120)

        if keyboard.is_pressed("space") and local_player:
            local_flags = pm.read_int(local_player + m_fFlags)
            local_fjump = (client + dwForceJump)
            if local_flags and local_flags == 257:
                pm.write_int(local_fjump, 6)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)
                pm.write_int( entity + m_bSpotted, 1 )

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(1))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow


if __name__ == '__main__':
    main()

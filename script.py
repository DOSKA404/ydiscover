import socket
import threading
import os
import libvirt
import sys

class Server:
    def __init__(self, port=8888):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        self.clients = {}
        self.allowed_clients = set()
        self.lock = threading.Lock()
        self.conn = libvirt.open('qemu:///system')  # Connexion à libvirt
        if self.conn is None:
            print('Échec de la connexion à libvirt. Assurez-vous que libvirt est installé et le service est en cours d\'exécution.')
            sys.exit(1)

        print(f"Serveur d'écoute démarré sur le port {port}")

    def create_vm(self, vm_name, memory=1024, vcpu=1, disk_size=10):
        # Code pour créer la machine virtuelle avec libvirt (QEMU/KVM)
        xml_desc = f"""
            <domain type='kvm'>
                <name>{vm_name}</name>
                <memory unit='KiB'>{memory * 1024}</memory>
                <vcpu placement='static'>{vcpu}</vcpu>
                <os>
                    <type arch='x86_64' machine='pc-i440fx-2.11'>hvm</type>
                    <boot dev='hd'/>
                </os>
                <devices>
                    <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='/var/lib/libvirt/images/{vm_name}.qcow2'/>
                        <target dev='vda' bus='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                    </disk>
                    <interface type='network'>
                        <mac address='52:54:00:00:00:01'/>
                        <source network='default'/>
                        <model type='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                    </interface>
                </devices>
            </domain>
        """

        try:
            dom = self.conn.createXML(xml_desc, 0)
            print(f"La machine virtuelle {vm_name} a été créée avec succès.")
            return True
        except libvirt.libvirtError as e:
            print(f"Erreur lors de la création de la machine virtuelle {vm_name}: {e}")
            return False

    # Les autres méthodes restent inchangées

    def start(self):
        try:
            while True:
                client_socket, addr = self.server.accept()
                username = client_socket.recv(1024).decode('utf-8').strip()
                
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr, username))
                client_handler.start()

        except KeyboardInterrupt:
            print("Arrêt du serveur.")
            self.server.close()

if __name__ == "__main__":
    server = Server()

    # Autoriser ou bloquer des clients en fonction de vos besoins
    server.authorize_client("utilisateur_autorise")
    server.block_client("utilisateur_bloque")

    # Création de machines virtuelles (à titre d'exemple)
    vm_configurations = [
        {"name": "vm1", "memory": 1024, "vcpu": 1, "disk_size": 10},
        {"name": "vm2", "memory": 2048, "vcpu": 2, "disk_size": 20},
        # Ajoutez d'autres configurations de VM selon vos besoins
    ]

    for vm_config in vm_configurations:
        server.create_vm(**vm_config)

    server.start()
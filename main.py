import tkinter as tk
from tkinter import ttk, filedialog
import os
import psutil

class VagrantFileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vagrant File Generator")

        # Obtenez les capacités du système
        self.total_memory = psutil.virtual_memory().total
        self.total_cpus = psutil.cpu_count(logical=False)
        self.total_storage = psutil.disk_usage('/').total  # Obtenez la capacité totale du stockage

        # Créer les étiquettes et les champs d'entrée
        self.iso_label = ttk.Label(root, text="Chemin vers le fichier ISO:")
        self.iso_entry = ttk.Entry(root, state='disabled')  # Définir l'état sur 'disabled' pour que l'utilisateur ne puisse pas éditer manuellement

        self.iso_browse_button = ttk.Button(root, text="Parcourir...", command=self.browse_iso)

        self.box_label = ttk.Label(root, text="Nom de la boîte (box):")
        self.box_entry = ttk.Entry(root, state='disabled')  # Définir l'état sur 'disabled' pour que l'utilisateur ne puisse pas éditer manuellement

        self.memory_label = ttk.Label(root, text="Quantité de mémoire:")
        self.memory_scale = ttk.Scale(root, from_=512, to=self.total_memory, orient=tk.HORIZONTAL, length=200, command=self.update_memory_label)
        self.memory_value_label = ttk.Label(root, text="0 MB")

        self.cpus_label = ttk.Label(root, text="Nombre de CPU:")
        self.cpus_scale = ttk.Scale(root, from_=1, to=self.total_cpus, orient=tk.HORIZONTAL, length=200, command=self.update_cpus_label)
        self.cpus_value_label = ttk.Label(root, text="1 CPU")

        self.storage_label = ttk.Label(root, text="Taille du stockage:")
        self.storage_scale = ttk.Scale(root, from_=1, to=self.total_storage, orient=tk.HORIZONTAL, length=200, command=self.update_storage_label)
        self.storage_value_label = ttk.Label(root, text="0 GB")

        self.network_type_label = ttk.Label(root, text="Type de réseau:")
        self.network_type_combobox = ttk.Combobox(root, values=["forwarded_port", "private_network", "public_network"])
        self.network_type_combobox.set("forwarded_port")  # Sélectionnez la première option par défaut

        self.network_ip_label = ttk.Label(root, text="Adresse IP du réseau:")
        self.network_ip_entry = ttk.Entry(root)

        self.username_label = ttk.Label(root, text="Nom d'utilisateur (admin):")
        self.username_entry = ttk.Entry(root)

        self.password_label = ttk.Label(root, text="Mot de passe (admin):")
        self.password_entry = ttk.Entry(root, show="*")

        # Créer le bouton de génération
        self.generate_button = ttk.Button(root, text="Générer Vagrantfile", command=self.generate_vagrant_file)

        # Organiser les éléments dans la grille
        self.iso_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.iso_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.iso_browse_button.grid(row=0, column=2, padx=10, pady=5)
        self.box_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.box_entry.grid(row=1, column=1, padx=10, pady=5)
        self.memory_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.memory_scale.grid(row=2, column=1, padx=10, pady=5)
        self.memory_value_label.grid(row=2, column=2, padx=10, pady=5)
        self.cpus_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.cpus_scale.grid(row=3, column=1, padx=10, pady=5)
        self.cpus_value_label.grid(row=3, column=2, padx=10, pady=5)
        self.storage_label.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.storage_scale.grid(row=4, column=1, padx=10, pady=5)
        self.storage_value_label.grid(row=4, column=2, padx=10, pady=5)
        self.network_type_label.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        self.network_type_combobox.grid(row=5, column=1, padx=10, pady=5)
        self.network_ip_label.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        self.network_ip_entry.grid(row=6, column=1, padx=10, pady=5)
        self.username_label.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
        self.username_entry.grid(row=7, column=1, padx=10, pady=5)
        self.password_label.grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)
        self.password_entry.grid(row=8, column=1, padx=10, pady=5)
        self.generate_button.grid(row=9, columnspan=3, pady=10)

    def update_memory_label(self, value):
        self.memory_value_label.config(text=f"{int(float(value))} MB")

    def update_cpus_label(self, value):
        self.cpus_value_label.config(text=f"{int(round(float(value)))} CPU")

    def update_storage_label(self, value):
        self.storage_value_label.config(text=f"{int(float(value) / (1024**3))} GB")  # Convertir en Go

    def browse_iso(self):
        iso_path = filedialog.askopenfilename(title="Sélectionner le fichier ISO", filetypes=[("ISO files", "*.iso")])
        if iso_path:
            self.iso_entry.config(state='normal')
            self.iso_entry.delete(0, tk.END)
            self.iso_entry.insert(0, iso_path)
            self.iso_entry.config(state='disabled')
            self.update_box_name()

    def update_box_name(self):
        # Extraire le nom du fichier de l'ISO
        iso_path = self.iso_entry.get()
        if iso_path:
            iso_filename = os.path.basename(iso_path)
            # Remplacer les espaces et les caractères spéciaux pour obtenir un nom de boîte valide
            box_name = iso_filename.replace(" ", "_").replace(".", "_").replace("-", "_")
            # Mettre à jour le champ de saisie de la boîte avec le nouveau nom
            self.box_entry.config(state='normal')
            self.box_entry.delete(0, tk.END)
            self.box_entry.insert(0, box_name)
            self.box_entry.config(state='disabled')

    def generate_vagrant_file(self):
        box_name = self.box_entry.get()
        memory = str(self.memory_scale.get())
        cpus = str(self.cpus_scale.get())
        storage = str(self.storage_scale.get())
        network_type = self.network_type_combobox.get()
        network_ip = self.network_ip_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validation des entrées peut être ajoutée ici si nécessaire

        # Génération du fichier Vagrant
        with open('Vagrantfile', 'w') as file:
            file.write(f'Vagrant.configure("2") do |config|\n')
            file.write(f'  config.vm.box = "{box_name}"\n')
            file.write(f'  config.vm.network "{network_type}", ip: "{network_ip}"\n')
            file.write(f'  config.vm.provider "virtualbox" do |vb|\n')
            file.write(f'    vb.memory = "{memory}"\n')
            file.write(f'    vb.cpus = {cpus}\n')
            file.write(f'    vb.customize ["modifyvm", :id, "--ioapic", "on"]\n')  # Activer l'APIC pour Windows
            file.write(f'    vb.customize ["modifyvm", :id, "--disk-size", {storage}]\n')  # Taille du disque
            file.write(f'  end\n')
            file.write(f'  config.vm.provision "shell", inline: <<-SHELL\n')
            file.write(f'    # Configurez le nom d\'utilisateur et le mot de passe de l\'administrateur\n')
            file.write(f'    sudo useradd -m -p "$(openssl passwd -1 {password})" {username}\n')
            file.write(f'    sudo usermod -aG sudo {username}\n')
            file.write(f'  SHELL\n')
            file.write(f'end\n')
        print("Fichier Vagrantfile généré avec succès.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VagrantFileGeneratorApp(root)
    root.mainloop()

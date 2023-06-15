import os
import shutil
import hashlib
import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import filedialog, messagebox

def create_incremental_backup():
    source_dir = source_dir_entry.get()
    backup_dir = backup_dir_entry.get()
    receiver_email = receiver_email_entry.get()

    if not source_dir or not backup_dir or not receiver_email:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Verifica se o diretório de backup existe, caso contrário, cria-o
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Contador de arquivos copiados
    count = 0

    # Percorre todos os arquivos do diretório de origem
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)
            backup_path = os.path.join(backup_dir, root[len(source_dir) + 1:], file)

            # Verifica se o arquivo existe no backup
            if os.path.exists(backup_path):
                # Calcula o hash do arquivo de origem
                source_hash = hash_file(source_path)

                # Calcula o hash do arquivo no backup
                backup_hash = hash_file(backup_path)

                # Compara os hashes
                if source_hash == backup_hash:
                    # Os arquivos são iguais, pula para o próximo
                    continue

            # Cria o diretório do arquivo no backup, se necessário
            backup_dir_path = os.path.dirname(backup_path)
            if not os.path.exists(backup_dir_path):
                os.makedirs(backup_dir_path)

            # Copia o arquivo de origem para o backup
            shutil.copy2(source_path, backup_path)
            print(f"Copiado: {source_path} -> {backup_path}")
            count += 1

    # Envia o e-mail de notificação com a contagem de arquivos copiados
    send_notification_email(count, receiver_email)
    messagebox.showinfo("Backup Concluído", f"O backup foi concluído com sucesso. {count} arquivos copiados.")

def hash_file(file_path):
    # Calcula o hash SHA-256 do arquivo
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def send_notification_email(count, receiver_email):
    # Configurações do servidor de e-mail
    smtp_server = "----------"
    smtp_port = 25

    # Configuração do e-mail
    sender = "e-mail de envio"
    SUBJECT = "Backup concluído"
    message = f"O backup foi concluído com sucesso. {count} arquivos copiados."

    # Cria o objeto MIMEText para o e-mail
    msg = MIMEText(message)
    msg['Subject'] = SUBJECT
    msg['From'] = sender
    msg['To'] = receiver_email

    # Conecta-se ao servidor de e-mail e envia o e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.send_message(msg)
        server.quit()

def browse_source_dir():
    directory = filedialog.askdirectory()
    if directory:
        source_dir_entry.delete(0, tk.END)
        source_dir_entry.insert(tk.END, directory)

def browse_backup_dir():
    directory = filedialog.askdirectory()
    if directory:
        backup_dir_entry.delete(0, tk.END)
        backup_dir_entry.insert(tk.END, directory)

root = tk.Tk()
root.title("Backup Incremental")

# Label e Entry para o diretório de origem
source_dir_label = tk.Label(root, text="Diretório de Origem:")
source_dir_label.grid(row=0, column=0, padx=10, pady=5)
source_dir_entry = tk.Entry(root)
source_dir_entry.grid(row=0, column=1, padx=10, pady=5)
source_dir_button = tk.Button(root, text="Procurar", command=browse_source_dir)
source_dir_button.grid(row=0, column=2, padx=10, pady=5)

# Label e Entry para o diretório de backup
backup_dir_label = tk.Label(root, text="Diretório de Backup:")
backup_dir_label.grid(row=1, column=0, padx=10, pady=5)
backup_dir_entry = tk.Entry(root)
backup_dir_entry.grid(row=1, column=1, padx=10, pady=5)
backup_dir_button = tk.Button(root, text="Procurar", command=browse_backup_dir)
backup_dir_button.grid(row=1, column=2, padx=10, pady=5)

# Label e Entry para o e-mail do destinatário
receiver_email_label = tk.Label(root, text="E-mail do Destinatário:")
receiver_email_label.grid(row=2, column=0, padx=10, pady=5)
receiver_email_entry = tk.Entry(root)
receiver_email_entry.grid(row=2, column=1, padx=10, pady=5)

# Botão para iniciar o backup
backup_button = tk.Button(root, text="Iniciar Backup", command=create_incremental_backup)
backup_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

root.mainloop()

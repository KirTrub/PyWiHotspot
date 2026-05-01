GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}===> Установка PyHotspot...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Ошибка: Python3 не установлен.${NC}"
    exit 1
fi

echo "--- Установка зависимостей через pip..."
pip3 install PyQt6 qrcode Pillow --break-system-packages 2>/dev/null || pip3 install PyQt6 qrcode Pillow

CURRENT_USER="${SUDO_USER:-$USER}"

echo "Настройка прав для пользователя: $CURRENT_USER"

sudo tee /etc/sudoers.d/pyhotspot > /dev/null << EOF
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/bin/nmcli
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/sbin/rfkill
$CURRENT_USER ALL=(ALL) NOPASSWD: /usr/sbin/sysctl -w net.ipv4.ip_forward=1
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl start NetworkManager
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl daemon-reload
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl enable pyhotspot.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl disable pyhotspot.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/rm -f /etc/systemd/system/pyhotspot.service
EOF

sudo chmod 440 /etc/sudoers.d/pyhotspot
sudo chown root:root /etc/sudoers.d/pyhotspot

if sudo visudo -c -f /etc/sudoers.d/pyhotspot; then
    echo "Права настроены успешно"
else
    echo "Ошибка в файле sudoers — удаляем"
    sudo rm /etc/sudoers.d/pyhotspot
    exit 1
fi

echo "--- Создание Desktop-файла..."
CAT_PATH=$(pwd)
cat <<EOF > pyhotspot.desktop
[Desktop Entry]
Name=PyHotspot
Comment=WiFi Hotspot Manager
Exec=python3 ${CAT_PATH}/core/main.py
Icon=network-wireless-hotspot
Terminal=false
Type=Application
Categories=Network;Settings;
EOF

chmod +x pyhotspot.desktop
mkdir -p ~/.local/share/applications
cp pyhotspot.desktop ~/.local/share/applications/

echo -e "${GREEN}===> Установка завершена!${NC}"
echo "Теперь вы можете запустить PyHotspot из меню приложений."
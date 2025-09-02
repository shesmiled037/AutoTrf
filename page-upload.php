<?php
// ================= CONFIG =================
$baseDir = __DIR__; // otomatis ke folder "page"
// ==========================================

// Ambil folder target dari POST (misal: "1")
$folder = isset($_POST['folder']) ? basename($_POST['folder']) : "default";

// Path folder tujuan
$targetDir = $baseDir . DIRECTORY_SEPARATOR . $folder;

// Buat folder kalau belum ada
if (!is_dir($targetDir)) {
    mkdir($targetDir, 0777, true);
}

// Cek apakah ada file diupload
if (isset($_FILES['file'])) {
    $uploadFile = $targetDir . DIRECTORY_SEPARATOR . basename($_FILES['file']['name']);
    
    if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
        echo json_encode([
            'success' => true,
            'file' => $uploadFile
        ]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Gagal upload']);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'Tidak ada file']);
}
?>

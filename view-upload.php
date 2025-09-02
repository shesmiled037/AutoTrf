<?php
if (!isset($_POST['slug']) || !isset($_FILES['file'])) {
    die("Missing slug or file");
}

$slug = preg_replace('/[^a-zA-Z0-9\-]/', '-', $_POST['slug']); // sanitize
$targetDir = __DIR__ . "/" . $slug;
if (!is_dir($targetDir)) {
    mkdir($targetDir, 0777, true);
}

$targetFile = $targetDir . "/index.html";
if (move_uploaded_file($_FILES["file"]["tmp_name"], $targetFile)) {
    echo "OK: $slug";
} else {
    echo "FAIL";
}

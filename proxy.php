<?php
if (!isset($_GET['url'])) {
    http_response_code(400);
    die("Missing URL");
}

$url = $_GET['url'];
$parsed = parse_url($url);
if ($parsed['host'] !== "stream.kingbokep.video") {
    http_response_code(403);
    die("Forbidden");
}

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
$response = curl_exec($ch);
$info = curl_getinfo($ch);
curl_close($ch);

$contentType = $info['content_type'] ?? 'application/vnd.apple.mpegurl';
header("Content-Type: $contentType");

// Kalau playlist .m3u8 → rewrite semua URL segmen
if (strpos($url, ".m3u8") !== false) {
    $baseUrl = $parsed['scheme'] . "://" . $parsed['host'];
    $dir = dirname($parsed['path']);
    
    $response = preg_replace_callback('/^(?!#)(.+)$/m', function($matches) use ($baseUrl, $dir) {
        $line = trim($matches[1]);
        if (preg_match('/^https?:\/\//', $line)) {
            // absolute URL → proxy-kan
            return "proxy.php?url=" . urlencode($line);
        } else {
            // relative URL → gabung base
            $realUrl = $baseUrl . $dir . "/" . $line;
            return "proxy.php?url=" . urlencode($realUrl);
        }
    }, $response);
}

echo $response;

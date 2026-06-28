<?php
$host = 'mysql';
$db   = 'app';
$user = 'app';
$pass = 'app';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database connection failed.");
}

$id = isset($_GET['id']) ? $_GET['id'] : '1';

$stmt = $pdo->query("SELECT username,email FROM users WHERE id=" . $id);
if ($stmt && $stmt->rowCount() > 0) {
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    echo "Username: " . $row['username'] . "<br>Email: " . $row['email'];
} else {
    echo "No user found.";
}

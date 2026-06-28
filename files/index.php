<?php
$host = 'mysql';
$db   = 'app';
$user = 'app';
$pass = 'app';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "<h1>PHP 7.2 + Nginx + MySQL</h1>";
    echo "<p>Database connected successfully!</p>";

    $stmt = $pdo->query("SHOW TABLES");
    $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);
    echo "<p>Tables: " . (count($tables) ? implode(', ', $tables) : 'none') . "</p>";

    phpinfo();
} catch (PDOException $e) {
    echo "<h1>PHP 7.2 + Nginx + MySQL</h1>";
    echo "<p>Database connection failed: " . $e->getMessage() . "</p>";
    phpinfo();
}

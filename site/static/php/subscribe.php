<?php
// The Keepers signup. Saves to a CSV one level ABOVE the web root (not publicly reachable) and notifies the MTT inbox.
$notify = 'momtriedthese@gmail.com';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /'); exit; }
if (!empty($_POST['website'])) { header('Location: /subscribed/'); exit; }
$email = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
if (!$email || strlen($email) > 200) { header('Location: /?signup=error#keepers'); exit; }
$name = substr(trim(preg_replace('/[\r\n,"]/', ' ', strip_tags($_POST['name'] ?? ''))), 0, 60);
$src = substr(preg_replace('/[^a-z0-9\/\-]/i', '', $_POST['src'] ?? ''), 0, 120);
$file = dirname(__DIR__) . '/mtt-keepers.csv';
$new = !file_exists($file);
$fh = @fopen($file, 'a');
if ($fh) { if (flock($fh, LOCK_EX)) { if ($new) fputcsv($fh, ['date','email','name','source']); fputcsv($fh, [gmdate('c'), $email, $name, $src]); flock($fh, LOCK_UN); } fclose($fh); }
@mail($notify, 'New Keepers signup: ' . $email, "Email: $email\nName: $name\nFrom page: $src\n", "From: Mom Tried These <hello@momtriedthese.com>\r\nContent-Type: text/plain; charset=UTF-8\r\n");
header('Location: /subscribed/'); exit;

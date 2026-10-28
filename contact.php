<?php
// Mom Tried These contact form. Sends to the MTT inbox. Honeypot + basic validation.
$to = 'momtriedthese@gmail.com';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/'); exit; }
if (!empty($_POST['website'])) { header('Location: /contact/thanks/'); exit; }
$name = trim(strip_tags($_POST['name'] ?? ''));
$email = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$topic = trim(strip_tags($_POST['topic'] ?? 'Message'));
$msg = trim(strip_tags($_POST['message'] ?? ''));
if (!$name || !$email || !$msg || strlen($msg) > 4000) { header('Location: /contact/?error=1'); exit; }
$name = str_replace(["\r", "\n"], ' ', $name); $topic = str_replace(["\r", "\n"], ' ', $topic);
$subject = 'Mom Tried These: ' . $topic . ' from ' . $name;
$body = "Name: $name\nEmail: $email\nTopic: $topic\n\n$msg\n";
$headers = "From: Mom Tried These <hello@momtriedthese.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=UTF-8\r\n";
@mail($to, $subject, $body, $headers);
header('Location: /contact/thanks/'); exit;

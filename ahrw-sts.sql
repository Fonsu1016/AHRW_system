-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2026-05-28 11:13:02
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `ahrw-sts`
--

-- --------------------------------------------------------

--
-- 資料表結構 `patients`
--

CREATE TABLE `patients` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `sex` enum('男','女') NOT NULL,
  `birth_date` date NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `risk_level` enum('低風險','中風險','高風險') DEFAULT NULL,
  `age` int(11) NOT NULL,
  `height` float NOT NULL,
  `weight` float NOT NULL,
  `BMI` float NOT NULL,
  `systolic_pressure` int(11) NOT NULL,
  `diastolic_pressure` int(11) NOT NULL,
  `pulse` int(11) NOT NULL,
  `temperature` float NOT NULL,
  `cholesterol` int(11) NOT NULL,
  `blood_sugar` int(11) NOT NULL,
  `smoking` enum('有','無') NOT NULL,
  `drinking` enum('有','無') NOT NULL,
  `exercise` enum('有','無') NOT NULL,
  `diagnose_result` text NOT NULL,
  `diabetes` enum('有','無') NOT NULL,
  `sleep_disorder` enum('有','無') NOT NULL,
  `diagnosis_time` timestamp NULL DEFAULT NULL,
  `overall_risk_score` float DEFAULT NULL,
  `systolic_pressure_p` float DEFAULT NULL,
  `diastolic_pressure_p` float DEFAULT NULL,
  `pulse_p` float DEFAULT NULL,
  `temperature_p` float DEFAULT NULL,
  `blood_sugar_p` float DEFAULT NULL,
  `cholesterol_p` float DEFAULT NULL,
  `smoking_p` float DEFAULT NULL,
  `drinking_p` float DEFAULT NULL,
  `exercise_p` float DEFAULT NULL,
  `diabetes_p` float DEFAULT NULL,
  `sleep_disorder_p` float DEFAULT NULL,
  `hypertension` enum('有','無') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `patients`
--

INSERT INTO `patients` (`user_id`, `name`, `sex`, `birth_date`, `phone`, `email`, `doctor_id`, `created_at`, `risk_level`, `age`, `height`, `weight`, `BMI`, `systolic_pressure`, `diastolic_pressure`, `pulse`, `temperature`, `cholesterol`, `blood_sugar`, `smoking`, `drinking`, `exercise`, `diagnose_result`, `diabetes`, `sleep_disorder`, `diagnosis_time`, `overall_risk_score`, `systolic_pressure_p`, `diastolic_pressure_p`, `pulse_p`, `temperature_p`, `blood_sugar_p`, `cholesterol_p`, `smoking_p`, `drinking_p`, `exercise_p`, `diabetes_p`, `sleep_disorder_p`, `hypertension`) VALUES
(1235450, '陳小王', '男', '1980-01-02', '0922222222', '1211@gmail.com', 4, '2025-07-22 08:00:00', '低風險', 50, 180, 75, 20, 105, 87, 65, 37, 50, 120, '無', '無', '有', '很好', '有', '有', '2026-05-27 07:07:01', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, ''),
(1234432892, '王小美', '女', '2000-01-01', '0912-345-678', 'wang.xiaomei@example.com', 1, '2025-10-19 05:25:59', '高風險', 20, 165, 50, 18.37, 150, 120, 100, 38, 200, 250, '有', '有', '無', '無', '無', '有', '2025-10-19 05:25:59', 96.41, 4.66, 2.07, 2.41, 5.34, 0, 0, 1.82, 3.06, 0, 0, 0, '有');

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `title` varchar(30) NOT NULL,
  `specialty` varchar(50) NOT NULL,
  `experience` int(100) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `age` int(100) NOT NULL,
  `history` varchar(100) NOT NULL,
  `phone` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `name`, `title`, `specialty`, `experience`, `gender`, `age`, `history`, `phone`, `email`, `address`) VALUES
(1, 'doctortest', '12345678', '吳小明', '主治醫師', '心臟內科', 20, '男', 49, 'XXXX醫院', 988888888, 'doctortestxxxxxx@gmail.com', '台中市X區XXXXXXXX25號'),
(4, 'doctortest2', '00000000', '吳大雄', '主治醫師', '心臟內科', 28, '男', 53, 'XXXX醫院', 988888888, 'doctortest2xxxxxx@gmail.com', '台中市X區XXXXXXXX25號');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `fk_doctor` (`doctor_id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `patients`
--
ALTER TABLE `patients`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1234432895;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

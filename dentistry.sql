-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 16, 2023 at 01:36 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dentistry`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `staff_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `username`, `password`, `staff_id`) VALUES
(5, 'admin', 'password', 4);

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('52257ec9a7dd');

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `admin_id` int(11) DEFAULT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `status` smallint(6) DEFAULT NULL COMMENT '0-pending, 1-approved, 2-completed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `patient_id`, `admin_id`, `appointment_date`, `appointment_time`, `status`) VALUES
(9, 14, 2, '2023-12-26', '08:30:00', 1),
(10, 15, 2, '2023-12-27', '08:30:00', 1),
(11, 15, 2, '2023-12-29', '08:30:00', 1),
(14, 17, 5, '2023-11-10', '08:30:00', 2),
(15, 18, 5, '2023-12-21', '08:07:00', 1),
(16, 19, 5, '2023-12-21', '08:30:00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `patient_id` int(11) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` smallint(6) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `treatment` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`patient_id`, `firstname`, `lastname`, `age`, `gender`, `contact_number`, `email`, `address`, `treatment`) VALUES
(1, 'Steph', 'qwe', 1, 0, 'asdfasdf', '11', '11', 'Dental Cleanings'),
(2, 'Steph', 'qwe', 1, 0, 'asdfasdf', '11', '11', 'Dental Cleanings'),
(3, 'Steph', 'qwqwe', 1, 0, '123', '123', '123', 'X-rays'),
(4, 'Steph', 'Aguilar', 21, 0, '9566046626', 'asdfhaskf@email.com', 'dasdfdfa', 'Emergency Dental Care'),
(5, 'Paanot', 'sadjfh', 123, 0, '129308129', 'qjehqw@gmail.com', 'asddd', 'Dental Examinations'),
(6, 'Steph', 'Marlboro', 21, 0, '9566046626', 'stephenonline25@gmail.com', 'unidentified', 'Preventive Education'),
(7, 'Steph', 'Marlboro', 21, 0, '9566046626', 'stephenonline25@gmail.com', 'unidentified', 'Preventive Education'),
(8, 'Steph', 'Marlboro', 21, 0, '9566046626', 'stephenonline25@gmail.com', 'unidentified', 'Preventive Education'),
(9, 'Steph', 'qwe', 12, 0, '123', '123', '123', 'Emergency Dental Care'),
(10, 'q', 'q', 11, 0, '123', '123', '123', 'Dental Examinations'),
(11, 'q', 'q', 11, 0, '12312', 'qweqw', 'qwe', 'Dental Examinations'),
(12, 'q', 'q', 11, 0, '12312', 'qweqw', 'qwe', 'Dental Examinations'),
(13, 'Steph', 'qwqwe', 1, 0, '1213', '12312', '3123123', 'hello'),
(14, 'Stephq', 'q', 123, 0, '213', 'qqweqw', '213', 'helloworld'),
(15, 'q', 'q', 111, 0, 'q', 'q', 'q', 'Fillings Treatment for dental cavities involving the removal of decayed tooth material and filling t'),
(16, 'q', 'q', 123, 0, 'q', 'q', 'q', 'Fillings'),
(17, 'Steph', 'Marlboro', 23, 0, '12313213', 'asdds@gmail.com', 'qweqwe', 'Dental Examinations'),
(18, 'Paanot', 'sadjfh', 21, 0, '11', '11', '11', 'Cosmetic Dentistry'),
(19, 'Exampple', 'Example', 11, 0, 'example', 'example', 'example', '13');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `service_title` varchar(100) NOT NULL,
  `service_description` varchar(255) NOT NULL,
  `service_price` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `service_title`, `service_description`, `service_price`) VALUES
(10, 'Tooth Extractions', 'Removal of damaged, decayed, or impacted teeth.', 500),
(11, 'Oral Surgery', 'Procedures such as wisdom tooth extraction, dental implant placement, and jaw surgery.', 1000),
(12, 'Gum Disease Treatment', 'Management of gum conditions like gingivitis and periodontitis through scaling, root planing, and surgical procedures.', NULL),
(13, 'Cosmetic Dentistry', 'Services like teeth whitening, veneers, bonding, and contouring to enhance the appearance of your teeth.', NULL),
(14, 'Oral Cancer Screening', 'Regular examinations to detect signs of oral cancer.', NULL),
(15, 'Temporomandibular Joint (TMJ) Treatment', 'Management of jaw joint disorders and associated pain.', NULL),
(16, 'Sedation Dentistry', 'Options for patients with dental anxiety, including nitrous oxide (laughing gas), oral sedatives, or intravenous (IV) sedation.', NULL),
(18, 'Emergency Dental Care', 'Treatment for dental emergencies such as severe toothache, broken teeth, or injuries.', NULL),
(19, 'Teeth Whitening', 'Professional teeth whitening procedures to enhance the color and brightness of your teeth.', NULL),
(20, 'Implant Dentistry', 'Placement of dental implants to replace missing teeth.', NULL),
(24, 'Pasta', '', 600),
(25, 'Trippings', 'Kahit anong description dito', 1000);

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `staff_id` int(11) NOT NULL,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `position` smallint(6) DEFAULT NULL COMMENT '0-master, 1-dentist, 2-hygienist, 3-receiptionist',
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`staff_id`, `firstname`, `lastname`, `position`, `contact_number`, `email`) VALUES
(4, 'Marlboro', 'Lights', 0, '09758274628', 'unidentified@domain.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`patient_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`staff_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `staff`
--
ALTER TABLE `staff`
  MODIFY `staff_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

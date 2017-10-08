-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 08, 2017 at 11:54 AM
-- Server version: 5.7.19-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fall_signup`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `level` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `name`, `password`, `level`) VALUES
(1, 'admin', '$2b$14$REDACTEDREDACTED!!!', 9001);

-- --------------------------------------------------------

--
-- Table structure for table `divisions`
--

CREATE TABLE `divisions` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `event_id` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `divisions`
--

INSERT INTO `divisions` (`id`, `name`, `description`, `event_id`) VALUES
(1, 'On-Site', 'This Division is for the actual on-site event at Augusta University. This Division is eligible for prizes and can consist of anyone and their brother. All are welcome!', 1),
(2, 'Remote', 'This Division is for those who can not make it to the on-site event at Augusta University. This Division is not eligible for prizes and can consist of anyone and their brother. All are welcome! (Though, we\'d much rather have you physically present, because reasons)', 1);

-- --------------------------------------------------------

--
-- Table structure for table `events`
--

CREATE TABLE `events` (
  `id` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description_fp` text NOT NULL,
  `description_full` text NOT NULL,
  `start` int(255) NOT NULL,
  `stop` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `events`
--

INSERT INTO `events` (`id`, `name`, `description_fp`, `description_full`, `start`, `stop`) VALUES
(1, 'CodeWarz Live - Fall 2017', 'CodeWarz Live at Augusta University! This is the 3rd iteration of CodeWarz being held at Augusta University. Doors open at 8am, competition starts at 9am and runs through 5pm. Prizes will be awarded for Top XXX places.', 'CodeWarz Live at <a href="http://www.augusta.edu/">Augusta University</a>! This is the 3rd iteration of CodeWarz being held at Augusta University.</p>\n<p>Doors open at 8am, competition starts at 9am and runs through 5pm. Prizes will be awarded for Top XXX places.</p>\n<p>\n<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3328.313172634133!2d-81.99141964906791!3d33.467196355685694!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x88f9cc36fc6feaeb%3A0x994eaa2b6edfd62a!2s1301+R.A.+Dent+Blvd%2C+Augusta%2C+GA+30901!5e0!3m2!1sen!2sus!4v1507471575833" width="600" height="450" frameborder="0" style="border:0" allowfullscreen></iframe>', 1510408800, 1510437600);

-- --------------------------------------------------------

--
-- Table structure for table `signups`
--

CREATE TABLE `signups` (
  `id` int(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `verified` int(255) NOT NULL,
  `hash` varchar(255) NOT NULL,
  `division` int(255) NOT NULL,
  `lang` text NOT NULL,
  `event_id` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `signups`
--

INSERT INTO `signups` (`id`, `username`, `email`, `verified`, `hash`, `division`, `lang`, `event_id`) VALUES
(2, 'leeterdude', 'leroy@jankins.biz', 1, 'aa82610d1ac174cc052cca32543f7307422cf44c7f79a883', 1, 'C', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `divisions`
--
ALTER TABLE `divisions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `signups`
--
ALTER TABLE `signups`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `divisions`
--
ALTER TABLE `divisions`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `events`
--
ALTER TABLE `events`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `signups`
--
ALTER TABLE `signups`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

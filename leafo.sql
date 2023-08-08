-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 08, 2023 at 05:19 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `leafo`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `ID` int(11) NOT NULL,
  `Nama` text NOT NULL,
  `username` varchar(10) NOT NULL,
  `password` text NOT NULL,
  `email` text NOT NULL,
  `No_HP` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`ID`, `Nama`, `username`, `password`, `email`, `No_HP`) VALUES
(3, 'Leonardo Fajar Mardika', 'lenk01', '$5$rounds=535000$k3USIW2D3oj7xtOZ$q6DBuTrJnD6p5iqvPrTiT7Bj03XDdmFfamCq6RC8y6B', 'fmleonardo107@gmail.com', '085727931988'),
(4, 'Asany', 'asany', '$5$rounds=535000$8HJ25aL8uCiRD5sm$nAJ/GSq1yTiQooyELwaj5crjiprWpLtfEKcvcM3mYEB', '', ''),
(5, 'Leonardo Fajar Mardika', 'leonardofm', '$5$rounds=535000$wmNFccTF9fokaMK2$KZn5kmAyvGY4cMD3OAAjVSf5TdxCQ9ejf7Q8/td0Ke3', 'fmleonardo107@gmail.com', '085727931988');

-- --------------------------------------------------------

--
-- Table structure for table `data_prediksi`
--

CREATE TABLE `data_prediksi` (
  `ID` int(11) NOT NULL,
  `Waktu` datetime DEFAULT NULL,
  `ID_Kebun` int(11) DEFAULT NULL,
  `UserID` varchar(100) DEFAULT NULL,
  `Nama_File` varchar(255) DEFAULT NULL,
  `Hasil_Prediksi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_prediksi`
--

INSERT INTO `data_prediksi` (`ID`, `Waktu`, `ID_Kebun`, `UserID`, `Nama_File`, `Hasil_Prediksi`) VALUES
(44, '2023-07-25 10:22:00', 1, 'fani', 'Prediksi3', 'Daun teh ini Sehat'),
(45, '2023-07-25 09:49:00', 3, 'fitri', 'Prediksi2', 'Daun teh ini Sakit'),
(46, '0000-00-00 00:00:00', 1, 'fani', 'Prediksi 4', 'Daun teh ini Sehat');

-- --------------------------------------------------------

--
-- Table structure for table `kebun`
--

CREATE TABLE `kebun` (
  `ID_Kebun` int(11) NOT NULL,
  `Latitude` varchar(100) NOT NULL,
  `Longitude` varchar(100) NOT NULL,
  `Alamat` text NOT NULL,
  `Blok` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kebun`
--

INSERT INTO `kebun` (`ID_Kebun`, `Latitude`, `Longitude`, `Alamat`, `Blok`) VALUES
(1, '-7.144795', '107.516395', 'Mekarsari, Kec. Pasirjambu, Kabupaten Bandung, Jawa Barat', ''),
(3, '-7.144910', '107.515573', 'PPTK Gambung, Mekarsari,Kec. Pasirjambu, Kabupaten Bandung, Jawa Barat', '5');

-- --------------------------------------------------------

--
-- Table structure for table `operator`
--

CREATE TABLE `operator` (
  `UserID` varchar(100) NOT NULL,
  `Nama_Operator` varchar(100) NOT NULL,
  `No_HP` varchar(20) DEFAULT NULL,
  `ID_Kebun` int(11) NOT NULL,
  `Alamat` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `operator`
--

INSERT INTO `operator` (`UserID`, `Nama_Operator`, `No_HP`, `ID_Kebun`, `Alamat`) VALUES
('asany', 'AsanyH', '12121', 3, '21312312312'),
('fani', 'Ibu Fani', '081827181811', 1, 'Mekarsari,Kec. Pasirjambu, Kabupaten Bandung, Jawa Barat'),
('fitri', 'Fitri', '08122938484', 3, 'Mekarsari,Kec. Pasirjambu, Kabupaten Bandung, Jawa Barat'),
('LenK01', 'Leonardo Fajar Mardika', '121212', 3, 'sadasdas'),
('Leonardo', 'Leonardo FM', '08122938484', 1, 'Mekarsari,Kec. Pasirjambu, Kabupaten Bandung, Jawa Barat');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `data_prediksi`
--
ALTER TABLE `data_prediksi`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID_Kebun` (`ID_Kebun`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `kebun`
--
ALTER TABLE `kebun`
  ADD PRIMARY KEY (`ID_Kebun`);

--
-- Indexes for table `operator`
--
ALTER TABLE `operator`
  ADD PRIMARY KEY (`UserID`),
  ADD KEY `ID_Kebun` (`ID_Kebun`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `data_prediksi`
--
ALTER TABLE `data_prediksi`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `kebun`
--
ALTER TABLE `kebun`
  MODIFY `ID_Kebun` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `data_prediksi`
--
ALTER TABLE `data_prediksi`
  ADD CONSTRAINT `data_prediksi_ibfk_1` FOREIGN KEY (`ID_Kebun`) REFERENCES `kebun` (`ID_Kebun`),
  ADD CONSTRAINT `data_prediksi_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `operator` (`UserID`);

--
-- Constraints for table `operator`
--
ALTER TABLE `operator`
  ADD CONSTRAINT `operator_ibfk_1` FOREIGN KEY (`ID_Kebun`) REFERENCES `kebun` (`ID_Kebun`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 17, 2025 at 06:27 AM
-- Server version: 8.0.31
-- PHP Version: 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `taphoa_hango`
--

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int NOT NULL,
  `label` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `label`, `name`, `description`) VALUES
(1, 'banh_keo', 'Bánh kẹo', 'Các loại bánh kẹo, snack'),
(2, 'bia', 'Bia', 'Bia các loại'),
(3, 'ca_phe', 'Cà phê', 'Cà phê hòa tan, cà phê rang xay'),
(4, 'dau_an', 'Dầu ăn', 'Dầu ăn các loại'),
(5, 'gia_vi', 'Gia vị', 'Gia vị nấu ăn'),
(6, 'mi_goi', 'Mì gói', 'Mì gói, mì ăn liền'),
(7, 'nuoc_mam', 'Nước mắm', 'Nước mắm các loại'),
(8, 'nuoc_ngot', 'Nước ngọt', 'Nước ngọt các loại, không bao gồm nước lọc'),
(9, 'nuoc_rua_chen', 'Nước rửa chén', 'Nước rửa chén'),
(10, 'nuoc_tuong', 'Nước tương', 'Nước tương, xì dầu'),
(11, 'sua', 'Sữa', 'Sữa tươi, sữa bột, sữa đặc');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int NOT NULL,
  `category_id` int NOT NULL,
  `product_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image_path` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `unit` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `notes` text COLLATE utf8mb4_general_ci,
  `description` text COLLATE utf8mb4_general_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `category_id`, `product_name`, `image_path`, `price`, `unit`, `notes`, `description`, `created_at`) VALUES
(6, 1, 'Nabati Phô Mai', 'z6558377390989_77a1bcd2de3590692d14ae8ba6bd5ffe-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:07:40'),
(8, 1, 'Cơm cháy chà bông', 'z6558377401943_1494a972a7b92a997d1d70aab879e18a-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:08:08'),
(10, 1, 'Bánh chà bông phô mai', 'z6558377402184_c300ba70a1e31014224b45663c934e6b-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:09:12'),
(11, 1, 'Nabati socola', 'z6558377404284_eb85f1169bfbffec78d61c461e6f92dc-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:09:38'),
(12, 1, 'ChocoPN', 'z6558377404540_d9bf2276a160f82f75aa16a6a8247018-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:10:02'),
(13, 1, 'Solite hộp', 'z6558377412949_e67d568813d8497fa02167b79deb386b-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:10:26'),
(14, 1, 'Karo trứng tươi chà bông', 'z6558377421880_1bf72bde35dde228d1524464caa86273-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:10:54'),
(15, 1, 'Bánh gạo One-One', 'z6558377429467_aea5dd0c32dbc7d76ba3ea6aa75d5b8c-removebg-preview (1).png', '0', '', NULL, NULL, '2025-05-01 09:11:14'),
(16, 1, 'Bánh quy coconut cracker', 'z6558377429468_c9a8c9baf92b39c65a046985138b1e48-removebg-preview (1).png', '0', '', NULL, NULL, '2025-05-01 09:11:32'),
(17, 1, 'Bánh quế Cosy vị lá dứa', 'z6558377446279_59ffb3acbcb7a9c320c9916d78958b79-removebg-preview', '0', '', NULL, NULL, '2025-05-01 09:12:01'),
(18, 1, 'Bánh quế Wafer Rolls vị lá dứa', 'z6558377448833_28015d683c50831510c86ef0acc384c8-removebg-preview (1).png', '0', '', NULL, NULL, '2025-05-01 09:12:41'),
(19, 1, 'Bánh quẩy', 'z6558377465333_66ed896685222f1e21382f1c0093b1e6-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:12:54'),
(20, 1, 'Cest Bon phô mai', 'z6558377466721_612f1364de5f8d886564d78325a57690-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:13:13'),
(21, 1, 'Nui chiên', 'z6558377486300_84555692300597e21a79c51a9ab83a59-removebg-preview.png', '0', '', NULL, NULL, '2025-05-01 09:13:25'),
(22, 2, 'Bia Hot Bias', 'z6558377303026_69c2fcc2cf71c66e82d7dbea3efb935d-removebg-preview (1).png', '0', '', NULL, NULL, '2025-05-02 00:28:44'),
(23, 2, 'Bia Tiger', 'z6558377322355_510a28dd09252430c5b61dc0c29fa8e1-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:29:58'),
(24, 2, 'Bia Sài Gòn Xanh', 'z6558377339452_e908253a7a7298323dab37f23d5d174e-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:30:54'),
(25, 3, 'Cà phê ống Trần Quang đen', 'z6558377377966_c0d314cc48481cdbf8df2787af204c30-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:32:24'),
(27, 3, 'Cà phê phố', 'z6558377381549_9477bb9ebcdc43e6a5bef5c0e8f6cd23-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:33:15'),
(28, 3, 'Cà phê Việt', 'z6558377383302_63d674b46f22e66f4c7f48fd7fa8b101-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:33:43'),
(29, 3, 'Bịch cà phê Trần Quang cam', 'z6558377390871_a40a0366bb945a3a1233d6216c9d807f-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:34:03'),
(30, 4, 'Dầu ăn Cái Lân lớn', 'z6558372875723_924f381e554461b9c792d679c8cdd4fc-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:35:00'),
(31, 4, 'Dầu ăn Cái Lân nhỏ', 'z6558372878735_fa98b6aa7c2acab5abd5a454895398c3-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:35:18'),
(32, 5, 'Nước màu', 'z6558372888930_25b67d70c4aa5626ddb42db0b7aaf6cf-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:36:32'),
(33, 5, 'Muối tây ninh', 'z6558372908090_28ef70aca610fd3ee67632cc01bfecd0-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:37:48'),
(34, 5, 'Tương ớt Chinsu', 'z6558372918619_c031f7ff82bf0cfdbf1bbaf1d5605e32-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:38:24'),
(35, 5, 'Chao Bông Mai tím', 'z6558372931243_55c0ee71d00d730dd8b7fcc7f79563ab-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:39:46'),
(36, 5, 'Chao Bông Mai Vàng', 'z6558372958340_c4efc85f4517f50ddbeb0168e2277f5f-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:41:18'),
(37, 5, 'Mắm tôm bắc', 'z6558375048385_153b5879382443bf13c76a03e77cf4a3-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:41:52'),
(38, 5, 'Bột rau câu con cá', 'z6558375066324_595a5afebe82418ee5727926b3ccd2ee-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:42:45'),
(39, 5, 'Muối Hảo Hảo', 'z6558375066695_bcebbdfa09f8f0bd79a8a08896a03599-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:43:45'),
(40, 5, 'Muối tiêu Bảo Ngọc', 'z6558375067969_dc459538c20c62fde29258a7d959c8fb-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:44:27'),
(41, 5, 'Bột canh A-One', 'z6558375068324_2ba5a7fcd41054580bd6892bc6283a25-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:45:02'),
(42, 5, 'Sa tế Ớt', 'z6558375089908_bf94b055ba6721f270f5ba859e5530b6-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:45:55'),
(43, 5, 'Knorr thịt kho tàu', 'z6558375092887_3855d177ba2faf36744193e005e3fac7-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:47:09'),
(44, 5, 'Knorr thịt kho', 'z6558375115706_1b3e09e519e6448bdb0cb11ab5d5a161-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:47:40'),
(45, 5, 'Tiêu đen bột', 'z6558375121034_7ff0cd1ae92471cefb87832ee5b9e03c-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:48:06'),
(46, 6, 'Cháo Gấu Đỏ', 'z6558372801913_e3f26e4f44c9d7bee2d45699f65f7ad7-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:49:36'),
(47, 6, 'Hủ tíu nhịp sống', 'z6558372815186_8feb258d220e3409c3321c20a01b7deb-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:50:13'),
(48, 6, 'Gấu Đỏ sợi phở', 'z6558372818445_802cc3cfafb6624fcbed842dc52a420e-removebg-preview (1).png', '0', '', NULL, NULL, '2025-05-02 00:51:00'),
(49, 6, 'Kokomi đại 90', 'z6558372832316_ea72341cd90ffbdb735fabdf1213b729-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:51:37'),
(50, 6, 'Mì Hảo Hảo', 'z6558372832680_6f5ee9ab7b1843c515edc2a378c05bb9-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:52:11'),
(51, 6, 'Mì 3 miền xanh', 'z6558372855888_d95664385a9d2b54b4077e5b2f2d019f-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:53:34'),
(52, 6, 'Gấu Đỏ tôm gà', 'z6558372856863_51c918480acbdec4e9ea53cdeac4e773-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:53:54'),
(53, 6, 'Bún giò heo', 'z6558372857054_7d8ba229b252129331e17ae6a36c305d-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:54:09'),
(54, 7, 'Chin su Đệ Nhị', 'z6558372789931_892a7a801720b5975c5a90d72ba8e4d8-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:55:05'),
(55, 7, 'Chinsu Nam Ngư', 'z6558372771179_10f492f03682675289e198c7bcf98188-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:55:53'),
(56, 8, 'Mirinda Cam lớn', 'z6558375129798_0a949f988fad928ab86b678b62b9f1d3-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:56:57'),
(57, 8, 'Mirinda xá sị', 'z6558375146221_1c0f16b0c877dfc50a15d7286f489891-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:57:39'),
(58, 8, 'Sting lớn', 'z6558375144106_b8ed6b550435d08320054d7a20ca5b5d-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:58:34'),
(59, 8, 'Pepsi Lớn', 'z6558375169658_14059f1ff998eb486269f7cfef1b6f98-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 00:59:16'),
(60, 8, 'Mirinda Xanh Lớn', 'z6558375181535_c58aea38ba873259f3fcb43b14fe7831-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:00:32'),
(61, 8, 'Coca Lớn', 'z6558375181908_a754a5def2f0ef3848d682ccc8a9b49b-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:01:01'),
(62, 8, 'Ô long lớn', 'z6558375214176_04998bdf7bed9c9181b23e036e58a91e-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:01:59'),
(63, 8, '7Up Lớn', 'z6558375225153_dc4760d2c31236494f9f90bf8b09a64e-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:04:21'),
(64, 8, 'C2 trà đào', 'z6558375226637_c392bf064707031623d28754f52b3528-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:04:51'),
(65, 8, 'Trà xanh không độ', 'z6558377284287_b9ce88204bf4ec759b151b26d9fab981-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:06:07'),
(66, 8, 'Wake up 247', 'z6558377267105_24bd4987102eda491e8b1103ffb8f2cb-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:06:24'),
(67, 8, 'Nước dừa chai', 'z6558377301004_9382fe37ef3c50b16bb326cfc955d258-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:06:36'),
(68, 8, 'C2 chanh', 'z6558377283152_ab56fe79d3fb2878b94748dc8c79aa41-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:06:50'),
(69, 8, 'Nước rửa chén Sunlight nhỏ', 'z6558372741039_bd6cdba71e9d7d540aeb9cce786f3b67-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:08:44'),
(70, 8, 'Nước rửa chén Sunlight lớn', 'z6558372761255_d77b053166fb3f0819f8b4a8fb94d684-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:09:04'),
(71, 9, 'Nước rửa chén Net can', 'z6558372733980_631cf6f3d3339237ed8529369a9e2305-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:09:52'),
(72, 10, 'Chin su Tam Thái Tử', 'z6558372721202_238431472ac1da4b075ac7616c9829da-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:11:00'),
(73, 11, 'Ngôi sao Phương Nam xanh lá', 'z6558377337605_c597ee0981f1fe47ecb32378f3080337-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:11:43'),
(74, 11, 'Ngôi sao Phương Nam xanh dương', 'z6558377357812_c839849083ef4424492e1fa000090aa3-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:12:20'),
(75, 11, 'Vinamilk 100% hộp', 'z6558377366120_dad1f73a28018e90ae283c7f9412fb33-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:13:01'),
(76, 11, 'Vinamilk 100% lốc', 'z6558377370839_7a21705540b3456eb5c366a0a0842d3c-removebg-preview.png', '0', '', NULL, NULL, '2025-05-02 01:13:24'),
(83, 3, 'Cà phê Trần Quang đen', 'z5834325940656_42a9d836cde110a620427e7458b31d90.jpg_421.jpg', '40000', 'bịch', NULL, NULL, '2025-05-03 04:01:27');

-- --------------------------------------------------------

--
-- Table structure for table `product_images`
--

CREATE TABLE `product_images` (
  `image_id` int NOT NULL,
  `product_id` int NOT NULL,
  `image_path` varchar(255) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_images`
--

INSERT INTO `product_images` (`image_id`, `product_id`, `image_path`) VALUES
(1, 22, 'z6558377302171_cbc9c26000eb2a09284aeeb9cbf372f1-removebg-preview.png'),
(2, 22, 'z6558377303026_69c2fcc2cf71c66e82d7dbea3efb935d-removebg-preview.png'),
(3, 23, 'z6558377317860_e620531c3e58c4af7dee6e8fae2a83df-removebg-preview.png'),
(4, 23, 'z6558377318519_a18864e06f738d3df884823d6685c6c8-removebg-preview.png'),
(5, 24, 'z6558377322468_d529214b10f3c92b7a6c6316268466c1-removebg-preview.png'),
(6, 24, 'z6558377338513_f6fcce6e8a6b79127788d7f404a4c589-removebg-preview.png'),
(7, 31, 'z6558372877484_ffaca2910cfef438c35540788261c04e-removebg-preview.png'),
(8, 32, 'z6558372892657_c6a026c3dc70d3fe54a7b1d430afae94-removebg-preview.png'),
(9, 33, 'z6558372902891_f301db4b6792b785d2e34c2e615ec2d1-removebg-preview.png'),
(10, 34, 'z6558372915429_2e80050ab0a5a880c240527ad59083be-removebg-preview (1).png'),
(11, 35, 'z6558372935287_d42c3e440bda66fd91c5deaae842b905-removebg-preview (1).png'),
(12, 35, 'z6558372942801_a2e1a73f0ba6bec66f7bf389e9bce8d4-removebg-preview.png'),
(13, 35, 'z6558372950385_79940e5bbe6f72d47e37b0c60ce9f0f4-removebg-preview.png'),
(14, 36, 'z6558372961918_58419dd74b40304cad1800ab47ca897a-removebg-preview.png'),
(15, 36, 'z6558375022928_d3d3b1833ce4e5732e037fa27a7bf3cc-removebg-preview.png'),
(16, 37, 'z6558375048386_fc00b960bf57f87b5d82614b3534b898-removebg-preview.png'),
(17, 36, 'z6558375050928_8ce5f753d42459708b63034698a669dd-removebg-preview.png'),
(18, 38, 'z6558375052675_527cb6d7b738443c2fc7b107dba17178-removebg-preview.png'),
(19, 40, 'z6558375067971_1d307ee797d3b3f4d7783dc086dee99d-removebg-preview.png'),
(20, 41, 'z6558375052682_e5bcfcf9aeff370b2ca42e178b6f47a5-removebg-preview.png'),
(21, 39, 'z6558375071986_d78c403df1694a41331c7d4f4c0be55e-removebg-preview.png'),
(22, 42, 'z6558375086321_5f96067423cbdc007040bd78af1f3a8b-removebg-preview.png'),
(23, 45, 'z6558375110233_d2173113d08e765912eb3c554c1828c5-removebg-preview.png'),
(24, 46, 'z6558372793873_211510b1673f02350729d89719526d5e-removebg-preview.png'),
(25, 47, 'z6558372815177_a282ceac2ce3a36bd610903c6e0e8eae-removebg-preview.png'),
(26, 48, 'z6558372801478_3ed56789b5f46cdd58c9d5314deba9da-removebg-preview.png'),
(27, 49, 'z6558372813975_29d2c52a04fb03b9863acf9e0eb8a899-removebg-preview.png'),
(28, 50, 'z6558372829110_46b6d1d1908f29eb9f216b3108f084f3-removebg-preview.png'),
(29, 49, 'z6558372813975_29d2c52a04fb03b9863acf9e0eb8a899-removebg-preview.png'),
(30, 53, 'z6558372849667_b645391abeda32549fe8802cef240d46-removebg-preview.png'),
(31, 52, 'z6558372832681_923ff4b45265f82bc969670a9c475314-removebg-preview.png'),
(32, 54, 'z6558372768525_d47de8a9596e606c45946c961921d29d-removebg-preview.png'),
(33, 54, 'z6558372770438_4a431494e523030b44ea17121300de80-removebg-preview.png'),
(34, 55, 'z6558372753167_dd649cb8708d483ef8cc4cdfa5efeed9-removebg-preview.png'),
(35, 55, 'z6558372774161_27b4163cad34b976ad54697e291c770d-removebg-preview.png'),
(36, 56, 'z6558375130869_cdf45146ffcad2bd74295b37f495fcc6-removebg-preview.png'),
(37, 57, 'z6558375149347_8f4f0c4fc291ab00198f2b963556c6b1-removebg-preview.png'),
(38, 57, 'z6558375151596_47e141fb4955e9fbc7d5eb81311b52f9-removebg-preview.png'),
(39, 58, 'z6558375128741_e1e585f2d2790320c9aee52b8678e6b7-removebg-preview.png'),
(40, 59, 'z6558375146342_01e05973d82bc69228dd6f6e147ec62e-removebg-preview.png'),
(41, 59, 'z6558375161500_28fb87302d67a1f7ad21a4a6685c5aa9-removebg-preview.png'),
(42, 60, 'z6558375175596_fa0a9f09653ab259439ff5a5e3653fd8-removebg-preview.png'),
(43, 61, 'z6558375181785_c12ac06a7622c2dcc2e0a3dd27974092-removebg-preview.png'),
(44, 60, 'z6558375188746_0f20a877112902c5c95370c03ea9c9d4-removebg-preview.png'),
(45, 56, 'z6558375213568_20c227e7731c28d2c1bd159192dc1df6-removebg-preview.png'),
(46, 62, 'z6558375193113_fad769755f4e3b21d52369b988fbecb5-removebg-preview.png'),
(47, 62, 'z6558375210115_1aaa8f5acb0cf0a44821ab4540dd4be1-removebg-preview.png'),
(48, 61, 'z6558375192972_48fd681df3a34e415a3ac6d1d147f059-removebg-preview.png'),
(49, 56, 'z6558375226969_03d98adee43415de382f1f46e4a6ffc1-removebg-preview.png'),
(50, 63, 'z6558375228851_325df59ca47e4705b5786bb78ba3bd14-removebg-preview.png'),
(51, 64, 'z6558377263244_f2e59ca7abc62e1e2c1da2e73d6ba28f-removebg-preview.png'),
(52, 65, 'z6558377266714_c4dba550e9e591513f1241f041077970-removebg-preview.png'),
(53, 68, 'z6558377287507_f825a3dd490ade076ac6799a8df17881-removebg-preview.png'),
(54, 67, 'z6558377283018_ef9ba41d6ba37129c7241ac75f073424-removebg-preview.png'),
(55, 69, 'z6558372729647_112b4c937f8469e94a8fee0f714d4358-removebg-preview.png'),
(56, 71, 'z6558372734573_f46ee0676ebfc587282d42b5368ddcdd-removebg-preview.png'),
(57, 70, 'z6558372747505_cdc76e41757d06260387c8e79d014874-removebg-preview.png'),
(58, 72, 'z6558372712851_3a7ff0949dcff3d47493fbd9ab21b62b-removebg-preview.png'),
(59, 72, 'z6558372733142_ea0da47d42799dbeb575e1638b74cd00-removebg-preview.png'),
(60, 73, 'z6558377343477_b2ce8606d805caa3fa1daed81486317c-removebg-preview.png'),
(61, 74, 'z6558377359111_6d212f4688deaa1268692a2d4a89c190-removebg-preview.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `label` (`label`),
  ADD KEY `idx_label` (`label`),
  ADD KEY `idx_name` (`name`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `idx_category_id` (`category_id`);

--
-- Indexes for table `product_images`
--
ALTER TABLE `product_images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `idx_product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT for table `product_images`
--
ALTER TABLE `product_images`
  MODIFY `image_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_images`
--
ALTER TABLE `product_images`
  ADD CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

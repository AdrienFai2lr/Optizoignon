-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : mer. 19 fév. 2025 à 17:20
-- Version du serveur : 8.0.41-0ubuntu0.24.04.1
-- Version de PHP : 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `summoners_war`
--

-- --------------------------------------------------------

--
-- Structure de la table `monsters`
--

CREATE TABLE `monsters` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `com2us_id` int DEFAULT NULL,
  `family_id` int DEFAULT NULL,
  `skill_group_id` int DEFAULT NULL,
  `image_filename` varchar(255) DEFAULT NULL,
  `element` varchar(20) DEFAULT NULL,
  `archetype` varchar(20) DEFAULT NULL,
  `base_stars` tinyint DEFAULT NULL,
  `natural_stars` tinyint DEFAULT NULL,
  `obtainable` tinyint(1) DEFAULT NULL,
  `can_awaken` tinyint(1) DEFAULT NULL,
  `is_awakened` tinyint(1) DEFAULT NULL,
  `awaken_level` tinyint DEFAULT NULL,
  `awaken_bonus` text,
  `awakens_to` int DEFAULT NULL,
  `awakens_from` int DEFAULT NULL,
  `leader_skill_id` int DEFAULT NULL,
  `hp` int DEFAULT NULL,
  `attack` int DEFAULT NULL,
  `defense` int DEFAULT NULL,
  `speed` int DEFAULT NULL,
  `crit_rate` int DEFAULT NULL,
  `crit_damage` int DEFAULT NULL,
  `resistance` int DEFAULT NULL,
  `accuracy` int DEFAULT NULL,
  `homunculus` tinyint(1) DEFAULT NULL,
  `farmable` tinyint(1) DEFAULT NULL,
  `fusion_food` tinyint(1) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `monster_runes`
--

CREATE TABLE `monster_runes` (
  `id` int NOT NULL,
  `monster_id` int NOT NULL,
  `rune_id` int NOT NULL,
  `slot_number` tinyint NOT NULL,
  `date_equipped` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `monster_skills`
--

CREATE TABLE `monster_skills` (
  `monster_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `slot` tinyint NOT NULL,
  `level` tinyint DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `runes`
--

CREATE TABLE `runes` (
  `id` int NOT NULL,
  `rune_id` bigint NOT NULL,
  `wizard_id` bigint NOT NULL,
  `occupied_type` tinyint DEFAULT NULL,
  `occupied_id` bigint DEFAULT NULL,
  `slot_no` tinyint NOT NULL,
  `rank` tinyint NOT NULL,
  `class` tinyint NOT NULL,
  `set_id` tinyint NOT NULL,
  `upgrade_limit` tinyint DEFAULT NULL,
  `upgrade_curr` tinyint DEFAULT NULL,
  `base_value` int DEFAULT NULL,
  `sell_value` int DEFAULT NULL,
  `pri_eff_type` int DEFAULT NULL,
  `pri_eff_value` int DEFAULT NULL,
  `prefix_eff_type` int DEFAULT NULL,
  `prefix_eff_value` int DEFAULT NULL,
  `quality` enum('rare','heroic','legendary') NOT NULL,
  `locked` tinyint(1) DEFAULT '0',
  `level` tinyint NOT NULL DEFAULT '0',
  `original_grade` enum('normal','magic','rare','heroic','legendary') NOT NULL,
  `current_grade` enum('normal','magic','rare','heroic','legendary') NOT NULL,
  `original_quality` tinyint NOT NULL,
  `is_ancient` tinyint(1) GENERATED ALWAYS AS (((`rank` = 15) and (`class` = 16))) VIRTUAL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `rune_stat_ranges`
--

CREATE TABLE `rune_stat_ranges` (
  `id` int NOT NULL,
  `stat_type_id` int NOT NULL,
  `is_ancient` tinyint(1) NOT NULL DEFAULT '0',
  `stars` tinyint NOT NULL,
  `substat_initial_min` float NOT NULL,
  `substat_initial_max` float NOT NULL,
  `substat_upgrade_min` float NOT NULL,
  `substat_upgrade_max` float NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `rune_substats`
--

CREATE TABLE `rune_substats` (
  `id` int NOT NULL,
  `rune_id` int NOT NULL,
  `stat_type_id` int NOT NULL,
  `stat_value` float NOT NULL,
  `upgrade_count` tinyint DEFAULT '0',
  `initial_value` float NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `rune_upgrades`
--

CREATE TABLE `rune_upgrades` (
  `id` int NOT NULL,
  `rune_id` int NOT NULL,
  `level_reached` tinyint NOT NULL,
  `stat_type_id` int NOT NULL,
  `old_value` float NOT NULL,
  `new_value` float NOT NULL,
  `upgrade_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `skills`
--

CREATE TABLE `skills` (
  `id` int NOT NULL,
  `com2us_id` int DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `description` text,
  `slot` tinyint NOT NULL,
  `cooldown` tinyint DEFAULT NULL,
  `hits` tinyint DEFAULT '1',
  `aoe` tinyint(1) DEFAULT '0',
  `max_level` tinyint DEFAULT NULL,
  `level_progress_description` text,
  `multiplier` varchar(50) DEFAULT NULL,
  `multiplier_formula_raw` text,
  `passive` tinyint(1) DEFAULT '0',
  `icon_filename` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ;

-- --------------------------------------------------------

--
-- Structure de la table `skill_levels`
--

CREATE TABLE `skill_levels` (
  `skill_id` int NOT NULL,
  `level` tinyint NOT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `slot_stat_constraints`
--

CREATE TABLE `slot_stat_constraints` (
  `id` int NOT NULL,
  `slot_no` tinyint NOT NULL,
  `stat_type_id` int NOT NULL,
  `can_be_main_stat` tinyint(1) NOT NULL DEFAULT '0',
  `can_be_sub_stat` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `stat_types`
--

CREATE TABLE `stat_types` (
  `id` int NOT NULL,
  `code` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `monsters`
--
ALTER TABLE `monsters`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_com2us_id` (`com2us_id`);

--
-- Index pour la table `monster_runes`
--
ALTER TABLE `monster_runes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `monster_slot_unique` (`monster_id`,`slot_number`),
  ADD KEY `rune_id` (`rune_id`);

--
-- Index pour la table `monster_skills`
--
ALTER TABLE `monster_skills`
  ADD PRIMARY KEY (`monster_id`,`skill_id`),
  ADD KEY `skill_id` (`skill_id`);

--
-- Index pour la table `runes`
--
ALTER TABLE `runes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rune_id` (`rune_id`),
  ADD KEY `idx_is_ancient` (`is_ancient`);

--
-- Index pour la table `rune_stat_ranges`
--
ALTER TABLE `rune_stat_ranges`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `stat_type_stars_ancient` (`stat_type_id`,`stars`,`is_ancient`);

--
-- Index pour la table `rune_substats`
--
ALTER TABLE `rune_substats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rune_id` (`rune_id`),
  ADD KEY `stat_type_id` (`stat_type_id`);

--
-- Index pour la table `rune_upgrades`
--
ALTER TABLE `rune_upgrades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rune_id` (`rune_id`),
  ADD KEY `stat_type_id` (`stat_type_id`);

--
-- Index pour la table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `idx_com2us_id` (`com2us_id`);

--
-- Index pour la table `skill_levels`
--
ALTER TABLE `skill_levels`
  ADD PRIMARY KEY (`skill_id`,`level`);

--
-- Index pour la table `slot_stat_constraints`
--
ALTER TABLE `slot_stat_constraints`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slot_stat_unique` (`slot_no`,`stat_type_id`),
  ADD KEY `stat_type_id` (`stat_type_id`);

--
-- Index pour la table `stat_types`
--
ALTER TABLE `stat_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `monster_runes`
--
ALTER TABLE `monster_runes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `runes`
--
ALTER TABLE `runes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `rune_stat_ranges`
--
ALTER TABLE `rune_stat_ranges`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `rune_substats`
--
ALTER TABLE `rune_substats`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `rune_upgrades`
--
ALTER TABLE `rune_upgrades`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `slot_stat_constraints`
--
ALTER TABLE `slot_stat_constraints`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `stat_types`
--
ALTER TABLE `stat_types`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `monster_runes`
--
ALTER TABLE `monster_runes`
  ADD CONSTRAINT `monster_runes_ibfk_1` FOREIGN KEY (`monster_id`) REFERENCES `monsters` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `monster_runes_ibfk_2` FOREIGN KEY (`rune_id`) REFERENCES `runes` (`id`);

--
-- Contraintes pour la table `monster_skills`
--
ALTER TABLE `monster_skills`
  ADD CONSTRAINT `monster_skills_ibfk_1` FOREIGN KEY (`monster_id`) REFERENCES `monsters` (`id`),
  ADD CONSTRAINT `monster_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`);

--
-- Contraintes pour la table `rune_stat_ranges`
--
ALTER TABLE `rune_stat_ranges`
  ADD CONSTRAINT `rune_stat_ranges_ibfk_1` FOREIGN KEY (`stat_type_id`) REFERENCES `stat_types` (`id`);

--
-- Contraintes pour la table `rune_substats`
--
ALTER TABLE `rune_substats`
  ADD CONSTRAINT `rune_substats_ibfk_1` FOREIGN KEY (`rune_id`) REFERENCES `runes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `rune_substats_ibfk_2` FOREIGN KEY (`stat_type_id`) REFERENCES `stat_types` (`id`);

--
-- Contraintes pour la table `rune_upgrades`
--
ALTER TABLE `rune_upgrades`
  ADD CONSTRAINT `rune_upgrades_ibfk_1` FOREIGN KEY (`rune_id`) REFERENCES `runes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `rune_upgrades_ibfk_2` FOREIGN KEY (`stat_type_id`) REFERENCES `stat_types` (`id`);

--
-- Contraintes pour la table `skill_levels`
--
ALTER TABLE `skill_levels`
  ADD CONSTRAINT `skill_levels_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`);

--
-- Contraintes pour la table `slot_stat_constraints`
--
ALTER TABLE `slot_stat_constraints`
  ADD CONSTRAINT `slot_stat_constraints_ibfk_1` FOREIGN KEY (`stat_type_id`) REFERENCES `stat_types` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

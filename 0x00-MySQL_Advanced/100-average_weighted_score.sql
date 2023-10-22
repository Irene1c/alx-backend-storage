-- script that creates a stored procedure that computes and store the average weighted score for a student

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
	DECLARE avg_weighted_score FLOAT;

	SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
	INTO avg_weighted_score
	FROM users
	INNER JOIN corrections ON users.id = corrections.user_id
	INNER JOIN projects ON corrections.project_id = projects.id
	WHERE users.id = user_id;

	UPDATE users SET average_score = avg_weighted_score WHERE users.id = user_id;
END
$$

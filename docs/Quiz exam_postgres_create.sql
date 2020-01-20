CREATE TABLE "users" (
	"id" serial NOT NULL,
	"name" serial(255) NOT NULL,
	"rank" serial NOT NULL DEFAULT '0',
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "quiz" (
	"id" serial NOT NULL,
	"id_user" bigint NOT NULL,
	"name" varchar(255) NOT NULL,
	"prog_lang" varchar(255) NOT NULL,
	"question_1" serial(255) NOT NULL,
	"question_2" serial(255) NOT NULL,
	"question_n" serial(255) NOT NULL,
	CONSTRAINT "quiz_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "quiz_options" (
	"id" serial NOT NULL,
	"id_questions" bigint NOT NULL,
	"option_1" varchar(255) NOT NULL,
	"option_2" varchar(255) NOT NULL,
	"option_n" varchar(255) NOT NULL,
	CONSTRAINT "quiz_options_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "quiz_correct_answers" (
	"id" serial NOT NULL,
	"id_q_options" bigint NOT NULL,
	"answer_1" varchar(255) NOT NULL,
	"answer_2" varchar(255) NOT NULL,
	"answer_n" varchar(255) NOT NULL,
	CONSTRAINT "quiz_correct_answers_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "user_answers" (
	"id" serial NOT NULL,
	"id_correct_answers" bigint NOT NULL,
	"id_user" bigint NOT NULL,
	"id_quiz" bigint NOT NULL,
	"user_answer_1" varchar(255) NOT NULL,
	"user_answer_2" varchar(255) NOT NULL,
	"user_answer_n" varchar(255) NOT NULL,
	CONSTRAINT "user_answers_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "quiz" ADD CONSTRAINT "quiz_fk0" FOREIGN KEY ("id_user") REFERENCES "users"("id");

ALTER TABLE "quiz_options" ADD CONSTRAINT "quiz_options_fk0" FOREIGN KEY ("id_questions") REFERENCES "quiz"("id");

ALTER TABLE "quiz_correct_answers" ADD CONSTRAINT "quiz_correct_answers_fk0" FOREIGN KEY ("id_q_options") REFERENCES "quiz_options"("id");

ALTER TABLE "user_answers" ADD CONSTRAINT "user_answers_fk0" FOREIGN KEY ("id_correct_answers") REFERENCES "quiz_correct_answers"("id");
ALTER TABLE "user_answers" ADD CONSTRAINT "user_answers_fk1" FOREIGN KEY ("id_user") REFERENCES "users"("id");
ALTER TABLE "user_answers" ADD CONSTRAINT "user_answers_fk2" FOREIGN KEY ("id_quiz") REFERENCES "quiz"("id");


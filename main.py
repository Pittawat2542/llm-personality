from pathlib import Path

import typer
from dotenv import load_dotenv
from loguru import logger
from rich.progress import track
from typing_extensions import Annotated

from src.llms.facade import get_llm
from src.models.experiment import Experiment
from src.models.experimental_result import ExperimentalResult
from src.models.personality_result import PersonalityResult
from src.models.result_record import ResultRecord
from src.prompts.personality import get_personality_prompt
from src.types.experiment import PersonalityType, InteractionType
from src.types.openai import ConversationHistory
from src.utils import parse_response

app = typer.Typer()


@app.command()
def evaluate_personality(model: Annotated[str, typer.Option("--model", "-m", help="Model to use")],
                         personality_type: Annotated[
                             PersonalityType, typer.Option("--personality", "-p", help="Personality type")],
                         interaction_type: Annotated[
                             InteractionType, typer.Option("--interaction", "-i", help="Interaction type")]):
    experiment_id = f"{personality_type}_{interaction_type}_{model}"
    logger.info(f"Running experiment {experiment_id}")

    output_path = Path("outputs") / experiment_id
    output_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output path: {output_path}")

    logger.add(output_path / "experiment.log")

    llm = get_llm(model)
    experiment = Experiment(id=experiment_id, personality_type=personality_type, interaction_type=interaction_type,
                            model_name=model, llm=llm)
    logger.info(f"Experiment: {experiment}")

    with open(Path("data") / "ipip50" / "questions.txt", "r") as file:
        questions = file.readlines()
        questions = [question.strip() for question in questions]

    logger.info(f"Loaded IPIP-50 questions: {len(questions)} questions")

    choices = ["1: Very Inaccurate", "2: Moderately Inaccurate", "3: Neither Accurate Nor Inaccurate",
               "4: Moderately Accurate", "5: Very Accurate"]

    experimental_result = ExperimentalResult(experiment=experiment, results=[])

    initial_history = []

    if personality_type is not PersonalityType.NO_PERSONALITY:
        initial_history.append({
            "role": "system",
            "content": get_personality_prompt(personality_type)
        })
        logger.info(f"Added personality prompt of type {personality_type} to history")

    history: ConversationHistory = initial_history

    if interaction_type is not InteractionType.ALL_AT_ONCE:
        i = 0
        for question in track(questions, description="Processing questions"):
            logger.info(f"Processing question: {question}")
            prompt = f"""You are answering a questionnaire. Answer the following question. The question has {len(choices)} choices.
            
Choices are:
{"\n".join(choices)}.

Answer each question with only the question index followed by a colon and then the number of the choice in one new line. For example, `x: y`. Do not include full answers in the same line.

It's a question from a personality test. Please answer honestly.

Question:
{question}

Answer:
"""

            history.append({
                "role": "user",
                "content": prompt
            })

            logger.info(f"Interacting with {model} with the following prompt:\n{history}")
            response = experiment.llm.generate_content(history)
            parsed_response = parse_response(response[0])

            result_record = ResultRecord(id=i, question=question, prompt=history, raw_output=response,
                                         parsed_output=parsed_response)
            i += 1
            experimental_result.results.append(result_record)
            logger.info(f"Added result record: {result_record}")

            if interaction_type is InteractionType.ONE_AT_A_TIME_NEW_CONTEXT:
                history = initial_history
                logger.info(f"Resetting history to initial history")
            else:
                history.append({
                    "role": "assistant",
                    "content": f"{response[0]}"
                })
                logger.info(f"Added assistant response to history")
    else:
        prompt = f"""You are answering a questionnaire. Answer the following questions. Each question has {len(choices)} choices.
        
Choices are:
{"\n".join(choices)}.

Answer each question with only the question index followed by a colon and then the number of the choice in one new line. For example, `x: y`. Do not include full answers in the same line.

It's a question from a personality test. Please answer honestly.

Question:
{"\n".join(questions)}

Answer:
"""
        history.append({
            "role": "user",
            "content": prompt
        })

        logger.info(f"Interacting with {model} with the following prompt:\n{history}")
        response = experiment.llm.generate_content(history)
        raw_parsed_response = response[0].splitlines()
        raw_parsed_response = [parse_response(line) for line in raw_parsed_response]

        i = 0
        for question, parsed_response in zip(questions, raw_parsed_response):
            result_record = ResultRecord(id=i, question=question, prompt=history, raw_output=response,
                                         parsed_output=int(parsed_response))
            i += 1
            experimental_result.results.append(result_record)
            logger.info(f"Added result record: {result_record}")

    experimental_result_path = output_path / "experimental_result.json"
    experimental_result_path.write_text(experimental_result.json(exclude={"experiment": {"llm"}}))
    logger.info(f"Saved experimental result to {experimental_result_path}")

    raw_scores = [result.parsed_output for result in experimental_result.results]

    if len(raw_scores) != 50:
        logger.error(f"Expected 50 raw scores, got {len(raw_scores)}")
        return

    extroversion = 20 + (raw_scores[0]) - (raw_scores[5]) + (raw_scores[10]) - (raw_scores[15]) + (raw_scores[20]) - (
        raw_scores[25]) + (raw_scores[30]) - (raw_scores[35]) + (raw_scores[40]) - (raw_scores[45])
    agreeableness = 14 - (raw_scores[1]) + (raw_scores[6]) - (raw_scores[11]) + (raw_scores[16]) - (raw_scores[21]) + (
        raw_scores[26]) - (raw_scores[31]) + (raw_scores[36]) + (raw_scores[41]) + (raw_scores[46])
    conscientiousness = 14 + (raw_scores[2]) - (raw_scores[7]) + (raw_scores[12]) - (raw_scores[17]) + (
        raw_scores[22]) - (raw_scores[27]) + (raw_scores[32]) - (raw_scores[37]) + (raw_scores[42]) + (raw_scores[47])
    emotional_stability = 38 - (raw_scores[3]) + (raw_scores[8]) - (raw_scores[13]) + (raw_scores[18]) - (
        raw_scores[23]) - (
                              raw_scores[28]) - (raw_scores[33]) - (raw_scores[38]) - (raw_scores[43]) - (
                              raw_scores[48])
    intellect = 8 + (raw_scores[4]) - (raw_scores[9]) + (raw_scores[14]) - (raw_scores[19]) + (raw_scores[24]) - (
        raw_scores[29]) + (raw_scores[34]) + (raw_scores[39]) + (raw_scores[44]) + (raw_scores[49])

    personality_result = PersonalityResult(intellect=intellect, conscientiousness=conscientiousness,
                                           extroversion=extroversion, agreeableness=agreeableness,
                                           emotional_stability=emotional_stability)
    experimental_result.personality_result = personality_result
    logger.info(f"Personality result: {personality_result}")

    personality_result_path = output_path / "personality_result.json"
    personality_result_path.write_text(personality_result.json())
    logger.info(f"Saved personality result to {personality_result_path}")

    experimental_result_path = output_path / "experimental_result.json"
    experimental_result_path.write_text(experimental_result.json(exclude={"experiment": {"llm"}}))
    logger.info(f"Saved experimental result to {experimental_result_path}")


@app.command()
def run_experiment(model: Annotated[str, typer.Option("--model", "-m", help="Model to use")]):
    all_personalities = [PersonalityType.EXTROVERSION, PersonalityType.AGREEABLENESS, PersonalityType.CONSCIENTIOUSNESS, 
                         PersonalityType.EMOTIONAL_STABILITY, PersonalityType.INTELLECT, PersonalityType.NO_PERSONALITY]
    all_interactions = [InteractionType.ALL_AT_ONCE, InteractionType.ONE_AT_A_TIME_NEW_CONTEXT,
                        InteractionType.ONE_AT_A_TIME_SAME_CONTEXT]

    for personality in all_personalities:
        for interaction in all_interactions:
            evaluate_personality(model, personality, interaction)


@app.command()
def analyse():
    result_files = Path("outputs").rglob("personality_result.json")

    with open(Path("outputs") / "personality_results.csv", "w") as file:
        file.write(f"personality_type,interaction_type,model,intellect,conscientiousness,extroversion,agreeableness,"
                   f"emotional_stability\n")

    for result in result_files:
        if result.parent.parent.name.startswith("V"):
            continue

        personality_type = result.parent.name.split("PersonalityType.")[1].split("_In")[0]
        interaction_type = result.parent.name.split("_InteractionType.")[1].split("_g")[0]
        model = "g" + result.parent.name.split("_g")[1]

        personality_result = PersonalityResult.parse_file(result)

        with open(Path("outputs") / "personality_results.csv", "a") as file:
            file.write(f"{personality_type},{interaction_type},{model},{personality_result.intellect},"
                       f"{personality_result.conscientiousness},{personality_result.extroversion},"
                       f"{personality_result.agreeableness},{personality_result.emotional_stability}\n")


if __name__ == "__main__":
    load_dotenv()
    app()

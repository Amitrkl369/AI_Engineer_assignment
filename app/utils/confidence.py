from typing import List
from app.models.schemas import MarksheetOutput, FieldValue, SubjectMark


def _avg_ocr_conf_for_value(value: str, tokens: List[dict]) -> float:
	if not value or not tokens:
		return 0.0
	words = [w for w in value.strip().split() if w]
	if not words:
		return 0.0
	confs = []
	for w in words:
		w_low = w.lower().strip(" ,.-")
		matches = [t for t in tokens if t["text"].lower().strip(" ,.-") == w_low]
		if not matches:
			matches = [t for t in tokens if w_low in t["text"].lower()]
		if matches:
			confs.append(sum(m["conf"] for m in matches) / len(matches))
		else:
			confs.append(0.0)
	return sum(confs) / len(confs) if confs else 0.0


def combine_confidences(result: MarksheetOutput, ocr_data: dict) -> MarksheetOutput:
	"""Combine LLM-provided confidences with OCR token confidences.

	Strategy:
	  - For each extracted textual field, derive an OCR confidence by averaging
		token confidences for matching words.
	  - Combine final confidence as 0.6 * llm_conf + 0.4 * ocr_conf (configurable later).
	"""
	tokens = ocr_data.get("tokens", []) if ocr_data else []

	cand = result.candidate
	for attr in [
		"name",
		"father_name",
		"mother_name",
		"roll_no",
		"registration_no",
		"dob",
		"exam_year",
		"board",
		"institution",
	]:
		field: FieldValue = getattr(cand, attr, None)
		if field is None:
			continue
		llm_conf = getattr(field, "confidence", 0.0) or 0.0
		val = getattr(field, "value", None) or ""
		ocr_conf = _avg_ocr_conf_for_value(val, tokens)
		field.confidence = round(0.6 * llm_conf + 0.4 * ocr_conf, 3)

	new_subjects: List[SubjectMark] = []
	for subj in result.subjects or []:
		if subj.subject:
			s_val = subj.subject.value or ""
			s_llm = subj.subject.confidence or 0.0
			s_ocr = _avg_ocr_conf_for_value(s_val, tokens)
			subj.subject.confidence = round(0.6 * s_llm + 0.4 * s_ocr, 3)
		if subj.max_marks:
			m_val = subj.max_marks.value or ""
			m_llm = subj.max_marks.confidence or 0.0
			m_ocr = _avg_ocr_conf_for_value(m_val, tokens)
			subj.max_marks.confidence = round(0.6 * m_llm + 0.4 * m_ocr, 3)
		if subj.obtained_marks:
			o_val = subj.obtained_marks.value or ""
			o_llm = subj.obtained_marks.confidence or 0.0
			o_ocr = _avg_ocr_conf_for_value(o_val, tokens)
			subj.obtained_marks.confidence = round(0.6 * o_llm + 0.4 * o_ocr, 3)
		if subj.grade:
			g_val = subj.grade.value or ""
			g_llm = subj.grade.confidence or 0.0
			g_ocr = _avg_ocr_conf_for_value(g_val, tokens)
			subj.grade.confidence = round(0.6 * g_llm + 0.4 * g_ocr, 3)
		new_subjects.append(subj)
	result.subjects = new_subjects

	if result.overall_result:
		orv = result.overall_result.value or ""
		or_llm = result.overall_result.confidence or 0.0
		or_ocr = _avg_ocr_conf_for_value(orv, tokens)
		result.overall_result.confidence = round(0.6 * or_llm + 0.4 * or_ocr, 3)

	if result.issue_date:
		idv = result.issue_date.value or ""
		id_llm = result.issue_date.confidence or 0.0
		id_ocr = _avg_ocr_conf_for_value(idv, tokens)
		result.issue_date.confidence = round(0.6 * id_llm + 0.4 * id_ocr, 3)
	if result.issue_place:
		ipv = result.issue_place.value or ""
		ip_llm = result.issue_place.confidence or 0.0
		ip_ocr = _avg_ocr_conf_for_value(ipv, tokens)
		result.issue_place.confidence = round(0.6 * ip_llm + 0.4 * ip_ocr, 3)

	result.confidence_explanation = (
		"Combined confidence = 0.6*LLM_conf + 0.4*OCR_conf. "
		"OCR confidence is token-average for matched words; LLM_conf is from model output."
	)

	return result

# Developer Overview

This project centres on a traditional horary engine.  The flow below shows how a question is processed from taxonomy resolution to final scoring.

## Data Flow

```
taxonomy.resolve ─▶ horary_engine.engine
      │                 │
      │                 ├─ calculate_chart (chart build)
      │                 ├─ calculate_enhanced_aspects
      │                 ├─ TraditionalReceptionCalculator
      │                 ├─ _analyze_enhanced_solar_condition
      │                 ├─ _check_enhanced_perfection
      │                 └─ aggregate (scoring)
```

1. **Taxonomy resolution** – `backend/taxonomy.py::resolve` maps the question category to houses and significators.
2. **Chart build** – `backend/horary_engine/engine.py::HoraryEngine.calculate_chart` constructs the `HoraryChart` with planets, houses, lunar aspects and solar analysis.
3. **Aspects** – `backend/horary_engine/aspects.py::calculate_enhanced_aspects` finds applying/separating aspects and lunar timing.
4. **Receptions** – `backend/horary_engine/reception.py::TraditionalReceptionCalculator.calculate_comprehensive_reception` determines mutual or one-way receptions.
5. **Solar conditions** – `backend/horary_engine/engine.py::_analyze_enhanced_solar_condition` classifies cazimi, combustion or freedom from the Sun.
6. **Perfection** – `backend/horary_engine/engine.py::_check_enhanced_perfection` inspects applying aspects, receptions and impediments between significators.
7. **Scoring** – `backend/horary_engine/aggregator.py::aggregate` (or DSL-aware `solar_aggregator.aggregate`) totals testimony weights into a numeric verdict.

## Key Files for Exploration

- `backend/taxonomy.py` – central category defaults and house/significator resolution.
- `backend/horary_engine/engine.py` – chart calculation and judgment helpers including `extract_testimonies`.
- `backend/horary_engine/aspects.py` – aspect and lunar timing routines.
- `backend/horary_engine/reception.py` – comprehensive reception logic.
- `backend/horary_engine/aggregator.py` and `backend/horary_engine/solar_aggregator.py` – scoring utilities.
- `backend/evaluate_chart.py` – orchestrates contract resolution, testimony extraction and aggregation.

This overview should help new contributors quickly locate the code responsible for each stage of the horary evaluation pipeline.

from .models import Event, Opportunity, Project, Resource


def campus_guide(query, study_year="all"):
    terms = {term.lower() for term in query.split() if len(term) > 2}
    sources = (
        (Resource, "Resource", "resources/"),
        (Event, "Event", "events/"),
        (Opportunity, "Opportunity", "opportunities/"),
        (Project, "Project", "projects/"),
    )
    matches = []
    for model, kind, path in sources:
        items = model.objects.filter(is_published=True)
        if study_year in {"fy", "sy", "ty"}:
            from django.db.models import Q
            items = items.filter(Q(study_year=study_year) | Q(study_year="all"))
        for item in items:
            searchable = " ".join(str(getattr(item, field, "")) for field in ("title", "description", "subject", "skills", "organisation", "category", "status")).lower()
            score = sum(2 if term in item.title.lower() else 1 for term in terms if term in searchable)
            if study_year in {"fy", "sy", "ty"} and item.study_year == study_year:
                score += 2
            if score:
                matches.append({"item": item, "kind": kind, "path": path, "score": score})
    return sorted(matches, key=lambda match: (-match["score"], -match["item"].created_at.timestamp()))[:8]

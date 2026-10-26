import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unit01 import get_unit_1
from unit02 import get_unit_2
from unit03 import get_unit_3
from unit04 import get_unit_4
from unit05 import get_unit_5
from unit06 import get_unit_6
from unit07 import get_unit_7
from unit08 import get_unit_8
from unit09 import get_unit_9
from unit10 import get_unit_10

all_units = {
    1: get_unit_1(),
    2: get_unit_2(),
    3: get_unit_3(),
    4: get_unit_4(),
    5: get_unit_5(),
    6: get_unit_6(),
    7: get_unit_7(),
    8: get_unit_8(),
    9: get_unit_9(),
    10: get_unit_10()
}

# Raw words extracted from the PDF pages OCR:
pdf_words_by_unit = {
    1: [
        "Bond", "Complex", "Behaviour", "Repeatedly", "Suffering", "Cognitive", "Recognition", 
        "Treat", "Grief", "Controversial", "Notion", "Engage in", "Take part in",
        "Observe", "Generally", "Previously", "Gender", "Intense", "Discipline", "Replace", 
        "Establish", "Mimic", "Offspring",
        "Prevent", "Preview", "Predict", "Previous", "Preschool",
        "Be similar to", "Both", "Like/Unlike", "Likewise", "Similarly", "While/Whereas", "On the other hand",
        "Focus on", "Influence", "Assume", "Factor", "Purchase", "Bargain", "Consumer", "React to", "Commercial", "Complex",
        "Aware", "Debt", "Concerned", "Estimate", "Fascinating", "Limit", "Productive", "Shortage", "Substitute", "Treat",
        "Extended family", "Social structure", "In captivity", "Immediate family", "Decision-makers", "Wildlife", "Eye contact"
    ],
    2: [
        "Examine", "Determine", "Mystery", "Analysis", "Detective", "Presence", "Identity", "Suspect", "Prove",
        "Advance", "Combination", "Consider", "Delicate", "Feature", "Medical", "Place", "Reveal", "Specialize in", "Trace",
        "Economy", "Economist", "Therapy", "Therapist", "Genetics", "Geneticist", "Pharmacy", "Pharmacist", "Emotion", "Emotional",
        "Face", "Facial", "Centre", "Central", "Controversy", "Controversial", "Resident", "Residential", "Politics", "Political",
        "Admit", "Infer", "Reconstruction",
        "Adapt", "Affect", "Trait", "Cautious", "Identical", "Circumstance", "Be exposed to", "Determine", "Investigate", "Unique", "Mispronounce",
        "Skilled", "Myth", "Exceptional", "Reject", "Dishonest", "Controversial", "Precise", "Sample", "Extreme", "Specific",
        "Interpersonal skills"
    ],
    3: [
        "Suburb", "Urban", "Urbanize", "Urbanization", "Income", "Productive", "Aspect", "Tend to", "Concentration", "Spread out", "Growth", "Dense",
        "Barrier", "Canal", "Construction", "Fierce", "Lower", "Occasional", "Partially", "Resident", "Separate", "Temporarily", "Disastrous", "Colossal", "Monitor",
        "Low-income", "Slow-moving", "Fast-moving", "Hard-earned",
        "Category", "Citizen", "Combination", "Illustrate", "Migration", "Poverty", "Settle",
        "Agriculture", "Come up with", "Growth", "Ignore", "Invest in", "Potential", "Refer", "Spread", "Supply",
        "Annual income", "Source of income", "Income tax", "Disposable income", "Income inequality", "Natural disaster", "Standard of living"
    ],
    4: [
        "Deadly", "Consequence", "Destruction", "Forecast", "Hazard", "Strike", "Alert", "Effectively", "Affordable", "Document", "Subtle",
        "Accumulate", "Collapse", "Continuous", "Crack", "Entire", "Eruption", "Explode", "Pressure", "Threaten", "Vast", "Exceptionally",
        "Threat", "Threaten", "Strength", "Strengthen", "Weak", "Weaken", "Height", "Heighten", "Light", "Lighten", "Dark", "Darken", "Flat", "Flatten",
        "Theory", "Theorize", "Critic", "Criticize", "Memory", "Memorize", "Social", "Socialize", "Special", "Specialize", "Stable", "Stabilize",
        "Appropriate", "Inappropriate", "Collapse", "Dramatic", "Dramatically", "Erosion", "Eventually", "Injury", "Layer", "Pressure", "Risk", "Surface", "Weakness", "Weaken", "Weakly",
        "Analysis", "Apparently", "Balance", "Compromise", "Consultant", "Harm", "Impact", "Look into", "Preserve",
        "In theory", "Find/get balance", "A major impact", "Come to/reach a compromise", "Cause/suffer harm", "Perform/carry out an analysis"
    ],
    5: [
        "Alternative", "Partnership", "Maintain", "Economy", "Preserve", "Necessary", "Sustainable", "Harmful", "Distinctive",
        "Objective", "Comfort", "Renewable", "Ecological", "Vital", "Awareness", "Landmark", "Spiritual", "Enrich", "Official", "Livelihood", "Indigenous",
        "Native", "Representative",
        "Finance", "Interact with", "Thoughtful", "Promote", "Alternative", "Role", "Strengthen", "Criticize", "Profit", "Recognize",
        "Entry-level", "Promotion", "Participate", "Dominate", "Feedback", "Reputation", "Effective", "Specialized", "Entire",
        "Earn a living", "Hot spot", "Make a difference"
    ],
    6: [
        "Availability", "Automatic", "Postpone", "Logical", "Multiple", "Contribute to", "Function", "Initially", "Conduct", "Flexible", "Gruelling",
        "Circumstance", "Command", "Mechanical", "Motor", "Signal", "Approval", "Distinguish", "Effective", "Praise", "Reality", "Associate with", "Verbal",
        "Autobiography", "Autopilot", "Automated", "Autograph", "Back up", "Stick out", "Try out",
        "Distinguish", "Absence", "Committed", "Element", "Function", "Concept", "Philosophy", "Material", "Date from", "Unfamiliar",
        "Priority", "Satisfaction", "Practical", "Enable", "Objective", "Browse", "Guarantee", "Crucial", "Adjustment", "Version"
    ],
    7: [
        "Crucial", "Currently", "Generate", "Related", "Shrink", "Vanish", "Exceptional", "Practical", "Worldwide", "Focus on",
        "Cut down on", "Emit", "Major", "Regulate", "Limited", "Exhaust", "Consume", "Consumption", "Convert", "Reduction", "Invest in",
        "Cut across", "Cut through", "A cut above", "Cut one’s losses", "Cut corners", "Cut one’s teeth",
        "Conservation", "Fatigue", "Get over", "Inspire", "Optimistic", "Paralyzed", "Passionate", "Perceive", "Pessimistic", "Resource",
        "Crisis", "Deny", "Depressing", "Discouraged", "Feature", "Give in", "Raise", "Run out of", "Renewable", "Stand for",
        "Take over", "Think over", "Hand over", "Talk Over", "Look over", "Hand in"
    ],
    8: [
        "Distraction", "Researcher", "Affect", "Discomfort", "Surgery", "Procedure", "Recovery", "Remarkable", "Addiction", "Version",
        "At risk", "Combine", "Constant", "Measure", "Specific", "Device", "Impressive", "Indicate", "Injury", "Diagnose",
        "Monitor", "Impact", "Continuous",
        "Remedy", "Symptom", "Drug", "Restore", "Poisonous", "Logical", "Reproduce", "Variable", "Predictable", "Approval",
        "Addicted", "Highlight", "Coincidence", "Make sense", "Condition", "Release", "Harmless", "Relief", "Heal", "Widely"
    ],
    9: [
        "Acquire", "Lead to", "Dynamic", "Linguistic", "Considerably", "Anticipate", "Competence", "Furthermore", "Expand", "Multilingual",
        "Biannual", "Monolingual", "Monorail", "Multilingual", "Multipurpose", "Triathlon", "Tricycle",
        "Archaeologist", "Claim", "Era", "Construct", "Mysterious", "Possession", "Range", "Represent", "Symbol", "Tool",
        "Civilization", "Collaboration", "Come to", "Curiosity", "Identity", "Individual", "Originally", "Propose", "Remains", "Specialist"
    ],
    10: [
        "Assistance", "Panic", "Civilization", "Priority", "Crisis", "Shelter", "Evacuate", "Supplies", "In the midst", "Tough",
        "Stay safe", "Stay informed", "Assist", "Assistance", "Appear", "Appearance", "Civilize", "Civilization", "Celebrate", "Celebration",
        "Perform", "Performance", "Disappear", "Disappearance", "Evacuate", "Evacuation", "Frustrate", "Frustration",
        "Universal", "Background", "Address", "Express", "Evident", "Occur", "Reaction", "Reflect", "Offensive",
        "Secure", "Significant", "Processed food", "Reduction", "Anxiety", "Mental health", "Boost", "Depression", "Stimulate", "Appetite"
    ]
}

def normalize(s):
    return re.sub(r"[^a-zA-Z]", "", s).lower()

missing_report = {}
for u, raw_list in pdf_words_by_unit.items():
    unit_words = all_units[u]
    unit_norm = {normalize(w["word"]): w for w in unit_words}
    
    # Also allow checking across all units if a word was covered in earlier units
    all_norm = {normalize(w["word"]): w for w_list in all_units.values() for w in w_list}
    
    missing_in_unit = []
    missing_anywhere = []
    for raw in raw_list:
        nr = normalize(raw)
        if nr not in unit_norm:
            # check if slash split, like Like/Unlike
            parts = [normalize(p) for p in re.split(r"[/–-]", raw)]
            if not any(p in unit_norm for p in parts):
                missing_in_unit.append(raw)
                if not any(p in all_norm for p in parts):
                    missing_anywhere.append(raw)
                    
    missing_report[u] = {
        "missing_in_unit": missing_in_unit,
        "missing_anywhere": missing_anywhere
    }

print("=== VERIFICATION SUMMARY ===")
total_missing_anywhere = 0
for u, rep in missing_report.items():
    print(f"Unit {u}:")
    print(f"  Missing in unit: {len(rep['missing_in_unit'])} -> {rep['missing_in_unit']}")
    print(f"  Missing ANYWHERE: {len(rep['missing_anywhere'])} -> {rep['missing_anywhere']}")
    total_missing_anywhere += len(rep['missing_anywhere'])

print(f"\nTotal words missing anywhere: {total_missing_anywhere}")

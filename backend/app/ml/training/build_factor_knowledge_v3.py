from __future__ import annotations

import json
import random
from itertools import combinations
from pathlib import Path


ROOT = Path("data/training/factor_corpus")
OUT = ROOT / "factor_knowledge_v3.jsonl"
PAIRS = ROOT / "factor_pairs_v3.jsonl"
SPLITS = ROOT / "splits_v3"


# Format:
# name | category | importance | uncertainty | evidence
#
# importance is contextual importance for THIS case.
# uncertainty is how uncertain IdX currently is about the factor.


CASES = [
    # ------------------------------------------------------------------
    # BUSINESS / HOSPITALITY
    # ------------------------------------------------------------------
    (
        "hotel_airport_business",
        "business",
        "hospitality",
        "airport_business_hotel",
        "Evaluate viability of a premium airport hotel for business travelers.",
        {
            "location": "near international airport",
            "customer": "business travelers",
            "rooms": 60,
        },
        [
            ("corporate booking demand", "customer", .96, .91,
             "corporate demand directly drives occupancy",
             ["corporate travel statistics", "business booking data"]),
            ("airport passenger demand", "market", .94, .90,
             "airport traffic establishes the available demand pool",
             ["airport passenger statistics"]),
            ("competitor room rates", "competition", .91, .84,
             "competitor pricing constrains achievable rates",
             ["competitor rates", "competitor positioning"]),
            ("expected occupancy", "economics", .95, .92,
             "occupancy is central to hotel revenue",
             ["historical occupancy", "comparable hotels"]),
            ("operating cost per room", "economics", .87, .82,
             "room economics determine contribution margin",
             ["staffing costs", "utilities", "maintenance"]),
            ("tourist arrival volume", "market", .48, .82,
             "tourist demand may contribute but is less aligned with the target",
             ["tourist arrival statistics"]),
            ("logo color", "branding", .00, .01,
             "does not materially determine commercial viability",
             []),
        ],
    ),
    (
        "hotel_tourist_resort",
        "business",
        "hospitality",
        "tourist_resort",
        "Evaluate a leisure resort in a seasonal tourist destination.",
        {
            "location": "tourist destination",
            "customer": "leisure travelers",
            "pricing": "mid-market",
        },
        [
            ("tourist arrival volume", "market", .98, .90,
             "visitor volume directly drives leisure demand",
             ["tourist arrivals"]),
            ("seasonality", "market", .97, .92,
             "seasonality can determine occupancy and cash flow",
             ["monthly tourism data"]),
            ("local attractions", "market", .86, .76,
             "attractions influence destination demand",
             ["visitor statistics"]),
            ("competitor room rates", "competition", .89, .83,
             "competitor rates constrain pricing",
             ["competitor rates"]),
            ("weekend occupancy", "economics", .81, .79,
             "leisure demand often concentrates on weekends",
             ["historical occupancy"]),
            ("corporate booking demand", "customer", .29, .84,
             "corporate demand is less aligned with leisure positioning",
             ["corporate travel data"]),
            ("employee uniform color", "operations", .01, .02,
             "not a material viability driver",
             []),
        ],
    ),
    (
        "restaurant_delivery",
        "business",
        "food_service",
        "delivery_restaurant",
        "Evaluate a delivery-first restaurant.",
        {
            "model": "delivery",
            "customer": "urban consumers",
            "average_order": "mid-range",
        },
        [
            ("local delivery demand", "market", .96, .88,
             "available local demand determines order volume",
             ["delivery order data", "population data"]),
            ("delivery radius", "operations", .90, .84,
             "radius determines reachable customers and delivery economics",
             ["delivery-time data"]),
            ("food cost percentage", "economics", .95, .86,
             "food costs directly affect contribution margin",
             ["supplier prices", "recipe costing"]),
            ("average order value", "economics", .91, .82,
             "order value determines revenue per delivery",
             ["transaction data"]),
            ("platform commission", "economics", .89, .90,
             "platform fees materially affect margins",
             ["platform contracts"]),
            ("menu complexity", "operations", .71, .74,
             "complex menus can affect preparation speed and waste",
             ["kitchen timing", "waste data"]),
            ("restaurant wall paint", "appearance", .01, .01,
             "not a primary delivery viability factor",
             []),
        ],
    ),
    (
        "marketplace_local_services",
        "business",
        "marketplace",
        "two_sided_local_marketplace",
        "Evaluate a marketplace connecting local service providers and customers.",
        {
            "supply": "fragmented providers",
            "customer": "local consumers",
            "geography": "single city",
        },
        [
            ("customer acquisition cost", "growth", .94, .88,
             "acquisition economics determine marketplace growth viability",
             ["marketing spend", "customer acquisition data"]),
            ("provider density", "supply", .92, .84,
             "sufficient supply is required for customer utility",
             ["provider counts"]),
            ("customer demand density", "demand", .96, .87,
             "demand density determines transaction potential",
             ["search volume", "transaction data"]),
            ("liquidity", "marketplace", .98, .93,
             "matching supply and demand is central to marketplace success",
             ["match rate", "time to match"]),
            ("take rate", "economics", .89, .82,
             "commission economics determine platform revenue",
             ["transaction economics"]),
            ("provider retention", "supply", .85, .90,
             "provider retention affects supply stability",
             ["provider churn"]),
            ("founder coding language", "technology", .02, .20,
             "implementation preference does not establish market viability",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # SOFTWARE / AI
    # ------------------------------------------------------------------
    (
        "saas_b2b",
        "business",
        "software",
        "b2b_saas",
        "Evaluate a B2B SaaS product for small businesses.",
        {
            "customer": "small businesses",
            "pricing": "subscription",
            "sales": "B2B",
        },
        [
            ("customer problem severity", "customer", 1.00, .93,
             "severe customer pain is fundamental to willingness to adopt",
             ["customer interviews", "usage data"]),
            ("willingness to pay", "customer", .98, .91,
             "willingness to pay determines commercial viability",
             ["pricing experiments"]),
            ("customer acquisition cost", "economics", .96, .89,
             "CAC determines growth economics",
             ["marketing data"]),
            ("retention", "customer", .99, .94,
             "retention determines recurring revenue durability",
             ["cohort retention"]),
            ("competitor differentiation", "competition", .91, .86,
             "differentiation affects customer choice",
             ["competitor analysis"]),
            ("market size", "market", .87, .78,
             "market size bounds long-term opportunity",
             ["market research"]),
            ("founder preferred language", "technology", .02, .10,
             "language preference does not establish business viability",
             []),
        ],
    ),
    (
        "saas_consumer",
        "business",
        "software",
        "consumer_subscription",
        "Evaluate a consumer subscription software product.",
        {
            "customer": "individual consumers",
            "pricing": "monthly subscription",
        },
        [
            ("conversion rate", "customer", .97, .89,
             "conversion determines how efficiently traffic becomes customers",
             ["funnel analytics"]),
            ("churn rate", "customer", 1.00, .95,
             "churn directly determines recurring revenue durability",
             ["cohort data"]),
            ("customer acquisition cost", "economics", .96, .91,
             "CAC determines acquisition economics",
             ["marketing data"]),
            ("price sensitivity", "customer", .93, .87,
             "consumer demand may vary strongly with price",
             ["pricing experiments"]),
            ("viral coefficient", "growth", .82, .80,
             "organic sharing can materially reduce acquisition costs",
             ["referral data"]),
            ("enterprise sales cycle", "sales", .14, .82,
             "enterprise sales are poorly aligned with the consumer model",
             ["sales pipeline"]),
            ("developer laptop brand", "technology", .01, .02,
             "not a meaningful commercial driver",
             []),
        ],
    ),
    (
        "ai_api_product",
        "technology",
        "artificial_intelligence",
        "ai_api_business",
        "Evaluate a commercial AI API product.",
        {
            "customer": "developers",
            "model": "hosted API",
            "pricing": "usage based",
        },
        [
            ("inference cost per request", "economics", .97, .91,
             "inference cost directly affects gross margin",
             ["cloud bills", "token usage"]),
            ("customer willingness to pay", "customer", .96, .88,
             "pricing power determines revenue potential",
             ["customer interviews", "pricing tests"]),
            ("model quality", "technology", .94, .83,
             "quality affects customer utility and retention",
             ["benchmark results", "production metrics"]),
            ("latency", "performance", .89, .82,
             "latency affects usability for interactive applications",
             ["production latency"]),
            ("retention", "customer", .92, .90,
             "retention determines recurring economics",
             ["cohort data"]),
            ("API reliability", "operations", .93, .86,
             "unreliable service creates customer churn and support costs",
             ["uptime", "incident history"]),
            ("office furniture", "operations", .00, .01,
             "not material to API product viability",
             []),
        ],
    ),
    (
        "developer_tool",
        "technology",
        "software",
        "developer_productivity_tool",
        "Evaluate a developer productivity tool.",
        {
            "customer": "software engineers",
            "distribution": "developer communities",
        },
        [
            ("developer workflow pain", "customer", .98, .91,
             "strong workflow pain drives adoption",
             ["developer interviews"]),
            ("time saved per task", "value", .97, .88,
             "measurable productivity improvement supports value",
             ["task benchmarks"]),
            ("integration friction", "technology", .91, .85,
             "difficult integration reduces adoption",
             ["installation data", "support tickets"]),
            ("developer retention", "customer", .94, .92,
             "continued usage validates product value",
             ["usage cohorts"]),
            ("distribution reach", "growth", .86, .84,
             "developer products require efficient distribution",
             ["community analytics"]),
            ("pricing sensitivity", "economics", .78, .81,
             "pricing affects conversion and monetization",
             ["pricing experiments"]),
            ("IDE icon color", "presentation", .00, .01,
             "not a primary adoption driver",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # MARKETS / HFT / FINANCE
    # ------------------------------------------------------------------
    (
        "trading_signal_short_horizon",
        "finance",
        "financial_markets",
        "systematic_short_horizon_strategy",
        "Determine whether a short-horizon trading signal is exploitable.",
        {
            "asset": "equities",
            "horizon": "short",
            "execution": "automated",
        },
        [
            ("out of sample predictive power", "research", 1.00, .96,
             "robust out-of-sample edge is necessary for credibility",
             ["walk-forward tests"]),
            ("transaction costs", "execution", .99, .89,
             "costs can eliminate theoretical edge",
             ["spread", "fees", "slippage"]),
            ("signal decay", "strategy", .97, .94,
             "short-horizon signals may decay quickly",
             ["half-life analysis"]),
            ("liquidity", "market", .95, .82,
             "liquidity determines achievable execution",
             ["market depth", "volume"]),
            ("market regime stability", "risk", .91, .93,
             "signal behavior may change across regimes",
             ["regime analysis"]),
            ("latency", "execution", .84, .81,
             "latency can materially affect short-horizon execution",
             ["execution timestamps"]),
            ("dashboard font", "presentation", .00, .01,
             "not related to trading edge",
             []),
        ],
    ),
    (
        "market_making_strategy",
        "finance",
        "financial_markets",
        "market_making",
        "Evaluate a systematic market-making strategy.",
        {
            "asset": "liquid equities",
            "execution": "automated",
        },
        [
            ("spread capture", "strategy", .97, .89,
             "spread capture is central to expected revenue",
             ["historical fills"]),
            ("adverse selection", "risk", .99, .94,
             "toxic flow can overwhelm spread revenue",
             ["post-trade price movement"]),
            ("inventory risk", "risk", .96, .91,
             "inventory exposure creates directional risk",
             ["inventory history"]),
            ("queue position", "execution", .92, .88,
             "queue position affects fill probability",
             ["order book data"]),
            ("latency", "execution", .94, .85,
             "latency affects quote competitiveness",
             ["order timestamps"]),
            ("transaction costs", "economics", .87, .79,
             "fees affect realized profitability",
             ["fee schedule"]),
            ("trading dashboard theme", "presentation", .00, .01,
             "not a driver of market-making economics",
             []),
        ],
    ),
    (
        "portfolio_strategy",
        "finance",
        "asset_management",
        "systematic_portfolio",
        "Evaluate a systematic multi-asset portfolio strategy.",
        {
            "assets": "equities and bonds",
            "horizon": "medium term",
        },
        [
            ("risk adjusted return", "performance", .98, .91,
             "risk-adjusted performance determines investment attractiveness",
             ["backtests", "live results"]),
            ("drawdown", "risk", .96, .90,
             "drawdown determines capital survivability",
             ["historical drawdown"]),
            ("factor exposure", "risk", .91, .85,
             "hidden exposures can explain portfolio behavior",
             ["factor attribution"]),
            ("correlation structure", "portfolio", .94, .89,
             "correlations determine diversification benefits",
             ["historical correlations"]),
            ("turnover", "execution", .82, .81,
             "turnover affects costs and tax efficiency",
             ["trade history"]),
            ("liquidity", "market", .88, .79,
             "illiquidity affects execution and exit risk",
             ["volume data"]),
            ("office lighting", "operations", .00, .01,
             "not a portfolio decision factor",
             []),
        ],
    ),
    (
        "fintech_lending",
        "finance",
        "fintech",
        "digital_lending",
        "Evaluate a digital lending product.",
        {
            "customer": "underserved borrowers",
            "model": "automated underwriting",
        },
        [
            ("default probability", "risk", .99, .94,
             "credit losses determine lending economics",
             ["historical repayment data"]),
            ("loss given default", "risk", .94, .88,
             "recovery determines realized credit losses",
             ["recovery data"]),
            ("customer acquisition cost", "growth", .89, .84,
             "CAC determines lending growth economics",
             ["marketing data"]),
            ("interest margin", "economics", .97, .91,
             "margin must cover expected losses and operating costs",
             ["loan economics"]),
            ("regulatory requirements", "regulation", .99, .96,
             "lending activity is constrained by applicable regulation",
             ["regulatory sources"]),
            ("fraud rate", "risk", .96, .93,
             "fraud can materially distort credit performance",
             ["fraud cases"]),
            ("app button color", "presentation", .01, .01,
             "not a primary lending viability factor",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # ENGINEERING / ROBOTICS
    # ------------------------------------------------------------------
    (
        "powered_exoskeleton",
        "engineering",
        "robotics",
        "powered_exoskeleton",
        "Determine technical feasibility of a wearable powered exoskeleton.",
        {
            "constraint": "wearable",
            "use_case": "human augmentation",
        },
        [
            ("battery energy density", "energy", 1.00, .94,
             "portable energy limits operating duration",
             ["battery specifications"]),
            ("actuator torque density", "mechanical", .99, .91,
             "actuators must provide required force within wearable mass",
             ["actuator specifications"]),
            ("system mass", "mechanical", .96, .84,
             "excess mass reduces usability and performance",
             ["prototype measurements"]),
            ("thermal management", "thermal", .94, .90,
             "heat generation constrains continuous operation",
             ["thermal testing"]),
            ("human safety", "safety", 1.00, .96,
             "failure can directly injure the wearer",
             ["safety tests"]),
            ("control stability", "control", .95, .89,
             "unstable assistance can make the system unsafe",
             ["control experiments"]),
            ("paint color", "appearance", .00, .01,
             "does not determine technical feasibility",
             []),
        ],
    ),
    (
        "autonomous_drone",
        "engineering",
        "robotics",
        "autonomous_delivery_drone",
        "Evaluate feasibility of autonomous package delivery by drone.",
        {
            "payload": "2 kg",
            "environment": "urban",
        },
        [
            ("payload to mass ratio", "mechanical", .96, .89,
             "payload efficiency determines practical flight capability",
             ["flight tests"]),
            ("battery endurance", "energy", .98, .94,
             "range and mission completion depend on available energy",
             ["flight logs"]),
            ("navigation reliability", "autonomy", .99, .93,
             "navigation failures can make autonomous operation unsafe",
             ["navigation tests"]),
            ("weather tolerance", "environment", .88, .91,
             "wind and precipitation constrain operating availability",
             ["weather tests"]),
            ("regulatory restrictions", "regulation", .97, .96,
             "airspace rules can constrain deployment",
             ["aviation regulations"]),
            ("landing accuracy", "operations", .85, .87,
             "delivery requires reliable landing or drop-off",
             ["landing tests"]),
            ("drone paint scheme", "appearance", .00, .01,
             "not a primary feasibility factor",
             []),
        ],
    ),
    (
        "battery_storage",
        "engineering",
        "energy",
        "grid_battery_storage",
        "Evaluate a stationary battery energy storage system.",
        {
            "application": "grid storage",
            "duration": "4 hours",
        },
        [
            ("round trip efficiency", "engineering", .94, .84,
             "efficiency affects usable energy and economics",
             ["system tests"]),
            ("battery degradation", "reliability", .97, .92,
             "degradation determines lifetime economics",
             ["cycle testing"]),
            ("capital cost per kWh", "economics", .99, .90,
             "capital intensity strongly affects project economics",
             ["vendor quotes"]),
            ("thermal safety", "safety", 1.00, .95,
             "thermal events create severe operational risk",
             ["safety tests"]),
            ("grid load profile", "demand", .96, .89,
             "storage value depends on when energy is needed",
             ["load data"]),
            ("cycle life", "reliability", .95, .91,
             "cycle life affects replacement requirements",
             ["manufacturer tests"]),
            ("container paint", "appearance", .00, .01,
             "not a material system factor",
             []),
        ],
    ),
    (
        "industrial_robot_cell",
        "engineering",
        "manufacturing",
        "robotic_manufacturing_cell",
        "Evaluate automation of a repetitive industrial assembly task.",
        {
            "task": "repetitive assembly",
            "volume": "high",
        },
        [
            ("cycle time", "operations", .98, .87,
             "cycle time determines production capacity",
             ["production measurements"]),
            ("robot utilization", "operations", .91, .83,
             "utilization affects capital productivity",
             ["machine logs"]),
            ("defect rate", "quality", .96, .86,
             "automation must maintain required quality",
             ["quality records"]),
            ("integration cost", "economics", .92, .89,
             "integration costs affect return on investment",
             ["vendor quotes"]),
            ("operator safety", "safety", .94, .93,
             "human interaction requires safe operation",
             ["safety assessment"]),
            ("maintenance downtime", "reliability", .87, .88,
             "downtime reduces effective production capacity",
             ["maintenance logs"]),
            ("robot color", "appearance", .00, .01,
             "not a primary automation decision factor",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # AGRICULTURE
    # ------------------------------------------------------------------
    (
        "commercial_crop_selection",
        "agriculture",
        "crop_production",
        "commercial_crop_selection",
        "Select a crop strategy for a small commercial farm.",
        {
            "farm_size": "2.5 acres",
            "region": "South India",
            "objective": "risk-adjusted return",
        },
        [
            ("soil conditions", "production", .98, .85,
             "soil suitability affects achievable yield",
             ["soil tests"]),
            ("water availability", "resources", 1.00, .91,
             "water availability constrains feasible crops",
             ["water assessment"]),
            ("expected yield", "production", .98, .90,
             "yield directly affects expected revenue",
             ["agronomic trials"]),
            ("market price", "market", .97, .87,
             "sale price determines gross revenue",
             ["market prices"]),
            ("weather risk", "risk", .96, .94,
             "weather can materially affect crop outcomes",
             ["weather history"]),
            ("crop duration", "production", .90, .82,
             "duration affects capital and land-use cycles",
             ["crop data"]),
            ("farmer favorite color", "irrelevant", .00, .01,
             "not relevant to crop economics",
             []),
        ],
    ),
    (
        "precision_irrigation",
        "agriculture",
        "agriculture",
        "precision_irrigation",
        "Evaluate whether precision irrigation can improve farm economics.",
        {
            "farm": "commercial",
            "problem": "water efficiency",
        },
        [
            ("baseline water consumption", "resources", .97, .88,
             "baseline usage determines potential savings",
             ["meter data"]),
            ("crop water requirement", "production", .98, .89,
             "irrigation demand varies by crop and growth stage",
             ["crop studies"]),
            ("irrigation efficiency", "engineering", .95, .86,
             "efficiency determines delivered water versus wasted water",
             ["field measurements"]),
            ("energy cost", "economics", .82, .80,
             "pumping costs affect economic savings",
             ["electricity bills"]),
            ("yield response", "production", .96, .92,
             "water optimization is valuable only if yield is maintained",
             ["field experiments"]),
            ("sensor reliability", "technology", .86, .87,
             "poor sensors can cause incorrect irrigation decisions",
             ["sensor validation"]),
            ("farm gate color", "appearance", .00, .01,
             "not material to irrigation economics",
             []),
        ],
    ),
    (
        "greenhouse_farming",
        "agriculture",
        "controlled_agriculture",
        "greenhouse",
        "Evaluate commercial greenhouse production.",
        {
            "crop": "high-value vegetable",
            "environment": "controlled",
        },
        [
            ("crop yield per area", "production", .98, .88,
             "yield density drives greenhouse revenue",
             ["production records"]),
            ("energy consumption", "economics", .94, .91,
             "controlled environments can have high energy costs",
             ["energy measurements"]),
            ("market selling price", "market", .97, .89,
             "high-value crops require sufficient price realization",
             ["market data"]),
            ("climate control reliability", "operations", .93, .90,
             "environmental failure can damage crops",
             ["equipment logs"]),
            ("labor cost", "economics", .86, .83,
             "labor affects operating margin",
             ["labor records"]),
            ("water efficiency", "resources", .84, .81,
             "water availability and efficiency constrain production",
             ["water measurements"]),
            ("greenhouse paint", "appearance", .00, .01,
             "not a primary production factor",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # ENERGY
    # ------------------------------------------------------------------
    (
        "renewable_microgrid",
        "engineering",
        "energy",
        "distributed_microgrid",
        "Evaluate a renewable distributed microgrid.",
        {
            "generation": "renewable",
            "system": "distributed",
        },
        [
            ("renewable resource availability", "resource", .98, .84,
             "resource availability determines generation potential",
             ["solar irradiance", "wind measurements"]),
            ("load profile", "demand", .96, .88,
             "generation and storage must match demand patterns",
             ["load measurements"]),
            ("storage requirement", "engineering", .97, .93,
             "storage bridges generation and demand mismatch",
             ["load and generation models"]),
            ("capital cost", "economics", .99, .87,
             "capital expenditure strongly affects project viability",
             ["vendor quotes"]),
            ("system efficiency", "engineering", .93, .78,
             "losses affect usable energy",
             ["system tests"]),
            ("grid reliability", "infrastructure", .90, .76,
             "grid availability affects backup value",
             ["outage records"]),
            ("enclosure color", "appearance", .00, .01,
             "not a primary project factor",
             []),
        ],
    ),
    (
        "ev_charging_station",
        "business",
        "energy",
        "ev_charging_network",
        "Evaluate an EV charging station investment.",
        {
            "location": "urban highway",
            "customers": "EV drivers",
        },
        [
            ("EV traffic volume", "demand", .98, .90,
             "station usage depends on EV traffic",
             ["traffic counts", "EV registrations"]),
            ("charger utilization", "operations", .96, .91,
             "utilization determines revenue generation",
             ["charging sessions"]),
            ("electricity tariff", "economics", .94, .87,
             "energy cost affects charging margins",
             ["utility tariff"]),
            ("installation cost", "economics", .92, .85,
             "upfront infrastructure cost affects return",
             ["vendor quotes"]),
            ("grid connection capacity", "infrastructure", .95, .89,
             "available electrical capacity constrains deployment",
             ["grid assessment"]),
            ("competitor charger density", "competition", .82, .80,
             "nearby alternatives influence demand",
             ["charger maps"]),
            ("charger casing color", "appearance", .00, .01,
             "not a primary investment driver",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # EDUCATION
    # ------------------------------------------------------------------
    (
        "adaptive_learning_platform",
        "education",
        "edtech",
        "adaptive_learning",
        "Evaluate an adaptive learning platform for students.",
        {
            "customer": "students",
            "delivery": "online",
        },
        [
            ("learning gain", "outcome", .99, .94,
             "educational effectiveness is the core product outcome",
             ["controlled assessments"]),
            ("student engagement", "customer", .91, .88,
             "engagement affects continued learning",
             ["usage analytics"]),
            ("completion rate", "customer", .90, .89,
             "students must complete material to realize learning benefits",
             ["course analytics"]),
            ("content quality", "education", .96, .87,
             "poor content limits educational value",
             ["expert review"]),
            ("personalization quality", "technology", .92, .90,
             "adaptation should match student needs",
             ["learning outcomes"]),
            ("customer acquisition cost", "economics", .77, .82,
             "acquisition economics determine commercial sustainability",
             ["marketing data"]),
            ("website gradient", "presentation", .00, .01,
             "not an educational effectiveness driver",
             []),
        ],
    ),
    (
        "coding_bootcamp",
        "education",
        "education",
        "coding_bootcamp",
        "Evaluate a coding education program.",
        {
            "students": "beginner developers",
            "goal": "employment",
        },
        [
            ("employment rate", "outcome", .99, .93,
             "employment is the stated student outcome",
             ["graduate outcomes"]),
            ("curriculum relevance", "education", .95, .86,
             "curriculum must match target jobs",
             ["job postings", "expert review"]),
            ("student completion", "customer", .92, .89,
             "completion is necessary for learning delivery",
             ["cohort data"]),
            ("mentor quality", "education", .88, .85,
             "mentorship can affect learning and persistence",
             ["student evaluations"]),
            ("tuition price", "economics", .84, .81,
             "price affects enrollment and accessibility",
             ["pricing analysis"]),
            ("placement partnerships", "employment", .90, .87,
             "employer connections can affect placement",
             ["employer data"]),
            ("classroom wall color", "appearance", .00, .01,
             "not a primary employment outcome driver",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # HEALTHCARE
    # ------------------------------------------------------------------
    (
        "diagnostic_device",
        "healthcare",
        "medical_device",
        "diagnostic_device",
        "Evaluate a new diagnostic device.",
        {
            "use": "clinical diagnosis",
            "setting": "hospital",
        },
        [
            ("diagnostic sensitivity", "clinical", .99, .94,
             "missed cases can materially harm patients",
             ["clinical validation"]),
            ("diagnostic specificity", "clinical", .99, .94,
             "false positives affect clinical decisions",
             ["clinical validation"]),
            ("clinical validation quality", "evidence", 1.00, .97,
             "clinical evidence determines whether performance claims are credible",
             ["clinical studies"]),
            ("regulatory approval", "regulation", .99, .96,
             "deployment depends on applicable regulatory requirements",
             ["regulatory documents"]),
            ("cost per test", "economics", .86, .83,
             "test economics affect adoption",
             ["cost analysis"]),
            ("test turnaround time", "operations", .90, .86,
             "speed can affect clinical workflow",
             ["workflow studies"]),
            ("device casing color", "appearance", .00, .01,
             "not a primary diagnostic factor",
             []),
        ],
    ),
    (
        "telemedicine_service",
        "healthcare",
        "healthcare",
        "telemedicine",
        "Evaluate a telemedicine service for remote patients.",
        {
            "patients": "rural",
            "delivery": "remote consultation",
        },
        [
            ("patient access", "customer", .97, .88,
             "the service must improve access to care",
             ["patient access data"]),
            ("clinical quality", "clinical", .99, .93,
             "remote care must remain clinically appropriate",
             ["clinical outcomes"]),
            ("doctor availability", "operations", .94, .90,
             "provider availability limits service capacity",
             ["scheduling data"]),
            ("connectivity reliability", "infrastructure", .93, .89,
             "poor connectivity can prevent consultations",
             ["network data"]),
            ("patient retention", "customer", .79, .84,
             "continued use affects service sustainability",
             ["patient cohorts"]),
            ("consultation cost", "economics", .83, .82,
             "affordability affects adoption",
             ["pricing analysis"]),
            ("app icon shape", "presentation", .00, .01,
             "not a primary healthcare outcome factor",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # MANUFACTURING / SUPPLY CHAIN
    # ------------------------------------------------------------------
    (
        "new_factory",
        "business",
        "manufacturing",
        "new_factory",
        "Evaluate a new industrial manufacturing operation.",
        {
            "product": "industrial component",
            "customer": "B2B",
        },
        [
            ("customer demand", "market", .98, .86,
             "production capacity is valuable only if demand exists",
             ["customer orders", "market research"]),
            ("unit production cost", "economics", 1.00, .91,
             "unit economics determine profitability",
             ["cost accounting"]),
            ("capacity utilization", "operations", .96, .88,
             "utilization affects fixed-cost absorption",
             ["production data"]),
            ("raw material cost", "supply_chain", .95, .84,
             "materials can materially affect unit economics",
             ["supplier prices"]),
            ("quality failure rate", "quality", .92, .80,
             "defects create cost and customer risk",
             ["quality records"]),
            ("supply chain reliability", "supply_chain", .89, .83,
             "supply disruptions can interrupt production",
             ["supplier history"]),
            ("factory wall color", "appearance", .00, .01,
             "not a primary manufacturing viability factor",
             []),
        ],
    ),
    (
        "warehouse_automation",
        "operations",
        "logistics",
        "automated_warehouse",
        "Evaluate automation for a high-volume warehouse.",
        {
            "volume": "high",
            "orders": "ecommerce",
        },
        [
            ("orders per hour", "demand", .93, .84,
             "volume determines required throughput",
             ["order history"]),
            ("picking time", "operations", .98, .87,
             "picking speed determines throughput",
             ["warehouse measurements"]),
            ("automation capital cost", "economics", .94, .86,
             "capital investment determines payback",
             ["vendor quotes"]),
            ("labor cost", "economics", .91, .82,
             "labor savings drive automation economics",
             ["labor records"]),
            ("error rate", "quality", .92, .84,
             "errors create returns and customer dissatisfaction",
             ["quality data"]),
            ("system downtime", "reliability", .90, .88,
             "downtime reduces throughput",
             ["system logs"]),
            ("warehouse wall branding", "appearance", .00, .01,
             "not a primary automation factor",
             []),
        ],
    ),
    (
        "supply_chain_risk",
        "operations",
        "supply_chain",
        "supplier_risk",
        "Assess supply-chain resilience for a critical product.",
        {
            "product": "electronics",
            "risk": "single-source dependency",
        },
        [
            ("supplier concentration", "risk", .99, .90,
             "single-source dependency creates disruption risk",
             ["supplier mapping"]),
            ("lead time variability", "operations", .95, .88,
             "variable lead times complicate inventory planning",
             ["supplier history"]),
            ("inventory buffer", "operations", .89, .84,
             "buffer inventory can mitigate supply interruptions",
             ["inventory data"]),
            ("supplier financial health", "risk", .92, .91,
             "supplier distress can create disruption",
             ["financial statements"]),
            ("alternative supplier availability", "supply_chain", .97, .93,
             "alternatives reduce dependency",
             ["supplier research"]),
            ("transportation reliability", "logistics", .86, .85,
             "transport disruptions affect delivery",
             ["carrier history"]),
            ("warehouse paint", "appearance", .00, .01,
             "not a supply-chain risk factor",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # SCIENCE / RESEARCH
    # ------------------------------------------------------------------
    (
        "battery_research",
        "science",
        "energy_research",
        "battery_chemistry",
        "Evaluate a new battery chemistry research direction.",
        {
            "goal": "higher energy density",
            "stage": "laboratory",
        },
        [
            ("measured energy density", "performance", .99, .94,
             "energy density is the primary research target",
             ["laboratory measurements"]),
            ("cycle stability", "reliability", .96, .92,
             "performance must persist across cycles",
             ["cycle tests"]),
            ("materials availability", "supply", .82, .80,
             "rare materials can limit scalability",
             ["materials sourcing"]),
            ("thermal stability", "safety", .98, .95,
             "thermal instability can prevent practical deployment",
             ["thermal testing"]),
            ("manufacturing compatibility", "scale", .91, .89,
             "laboratory performance may not translate to manufacturability",
             ["pilot manufacturing"]),
            ("measurement reproducibility", "research", 1.00, .97,
             "unreproducible results cannot support a research conclusion",
             ["replication experiments"]),
            ("lab wall color", "appearance", .00, .01,
             "irrelevant to scientific validity",
             []),
        ],
    ),
    (
        "drug_research",
        "science",
        "biomedical_research",
        "drug_candidate",
        "Evaluate a drug candidate for further development.",
        {
            "stage": "preclinical",
            "target": "disease pathway",
        },
        [
            ("efficacy evidence", "clinical", .99, .95,
             "evidence of biological effect determines development value",
             ["preclinical studies"]),
            ("toxicity", "safety", 1.00, .96,
             "toxicity can terminate development",
             ["toxicology studies"]),
            ("target specificity", "mechanism", .91, .89,
             "specificity can affect efficacy and side effects",
             ["mechanistic studies"]),
            ("dose response", "clinical", .94, .91,
             "dose response informs therapeutic window",
             ["dose-response studies"]),
            ("manufacturing feasibility", "scale", .81, .84,
             "development requires scalable production",
             ["process studies"]),
            ("reproducibility", "research", .98, .96,
             "reproducible evidence is necessary for confidence",
             ["replication studies"]),
            ("packaging color", "appearance", .00, .01,
             "not a development-stage scientific factor",
             []),
        ],
    ),

    # ------------------------------------------------------------------
    # PRODUCT / HARDWARE
    # ------------------------------------------------------------------
    (
        "consumer_smart_device",
        "business",
        "consumer_electronics",
        "smart_device",
        "Evaluate a new consumer smart device.",
        {
            "customer": "mass market",
            "category": "connected hardware",
        },
        [
            ("customer problem", "customer", .98, .91,
             "the product must solve a meaningful problem",
             ["customer research"]),
            ("bill of materials", "economics", .96, .88,
             "hardware margin depends on production cost",
             ["supplier quotes"]),
            ("battery life", "performance", .92, .86,
             "battery performance affects user experience",
             ["device testing"]),
            ("reliability", "quality", .96, .91,
             "hardware failures create returns and reputation damage",
             ["reliability tests"]),
            ("manufacturing yield", "operations", .94, .89,
             "low yield increases effective production cost",
             ["factory data"]),
            ("retail price", "economics", .93, .85,
             "price determines accessibility and margin",
             ["pricing research"]),
            ("box color", "appearance", .07, .10,
             "may affect branding but is not a primary viability factor",
             ["consumer testing"]),
        ],
    ),
    (
        "wearable_health_device",
        "product",
        "consumer_health",
        "health_wearable",
        "Evaluate a wearable device for health monitoring.",
        {
            "customer": "consumers",
            "use": "continuous monitoring",
        },
        [
            ("measurement accuracy", "performance", .99, .94,
             "incorrect measurements undermine product value",
             ["validation studies"]),
            ("battery life", "engineering", .94, .87,
             "continuous monitoring requires adequate endurance",
             ["battery tests"]),
            ("user adherence", "customer", .96, .92,
             "health insights require sustained usage",
             ["usage cohorts"]),
            ("false positive rate", "risk", .97, .93,
             "false alerts can cause harm and reduce trust",
             ["validation studies"]),
            ("regulatory classification", "regulation", .94, .96,
             "claims and deployment may be regulated",
             ["regulatory assessment"]),
            ("manufacturing cost", "economics", .84, .81,
             "cost affects commercial margins",
             ["supplier quotes"]),
            ("strap color", "appearance", .05, .08,
             "can affect preference but is secondary to measurement quality",
             ["consumer testing"]),
        ],
    ),

    # ------------------------------------------------------------------
    # GENERAL STRATEGY / OPERATIONS
    # ------------------------------------------------------------------
    (
        "new_retail_store",
        "business",
        "retail",
        "physical_retail",
        "Evaluate opening a new physical retail store.",
        {
            "location": "urban",
            "product": "consumer goods",
        },
        [
            ("foot traffic", "demand", .97, .89,
             "physical traffic creates the potential customer pool",
             ["footfall measurements"]),
            ("conversion rate", "customer", .94, .87,
             "conversion turns visitors into transactions",
             ["store analytics"]),
            ("average basket value", "economics", .92, .84,
             "basket value drives revenue per customer",
             ["transaction data"]),
            ("rent", "economics", .96, .91,
             "rent is a major fixed cost",
             ["lease terms"]),
            ("local competition", "competition", .88, .82,
             "competition affects demand and pricing",
             ["competitor research"]),
            ("inventory turnover", "operations", .86, .85,
             "slow inventory ties up capital",
             ["inventory records"]),
            ("storefront color", "appearance", .09, .15,
             "branding may have a secondary effect",
             ["consumer tests"]),
        ],
    ),
    (
        "subscription_media",
        "business",
        "media",
        "subscription_media",
        "Evaluate a paid digital media subscription.",
        {
            "customer": "consumers",
            "content": "premium",
        },
        [
            ("subscriber willingness to pay", "customer", .98, .90,
             "customers must value the content enough to subscribe",
             ["pricing experiments"]),
            ("churn", "customer", .99, .94,
             "churn determines subscription durability",
             ["cohort data"]),
            ("content production cost", "economics", .91, .86,
             "content cost affects margins",
             ["production budgets"]),
            ("subscriber acquisition cost", "growth", .93, .88,
             "CAC affects growth economics",
             ["marketing data"]),
            ("content differentiation", "competition", .94, .89,
             "unique content can reduce substitution",
             ["competitor analysis"]),
            ("engagement frequency", "customer", .89, .85,
             "engagement can influence retention",
             ["usage analytics"]),
            ("logo animation", "presentation", .00, .01,
             "not a primary subscription economics factor",
             []),
        ],
    ),
    (
        "logistics_last_mile",
        "operations",
        "logistics",
        "last_mile_delivery",
        "Optimize last-mile delivery economics.",
        {
            "orders": "urban ecommerce",
            "fleet": "delivery vehicles",
        },
        [
            ("delivery density", "operations", .99, .91,
             "dense routes reduce cost per delivery",
             ["route data"]),
            ("cost per delivery", "economics", .98, .89,
             "unit delivery economics determine profitability",
             ["cost accounting"]),
            ("delivery time", "customer", .93, .86,
             "service level affects customer satisfaction",
             ["delivery timestamps"]),
            ("vehicle utilization", "operations", .91, .84,
             "utilization affects fleet economics",
             ["fleet telemetry"]),
            ("failed delivery rate", "operations", .90, .88,
             "failed deliveries increase cost",
             ["delivery records"]),
            ("fuel or energy cost", "economics", .87, .85,
             "energy is a material operating expense",
             ["fuel bills"]),
            ("vehicle paint", "appearance", .00, .01,
             "not a primary logistics optimization factor",
             []),
        ],
    ),
    (
        "cloud_infrastructure",
        "technology",
        "cloud",
        "cloud_platform",
        "Evaluate a cloud infrastructure architecture.",
        {
            "workload": "high traffic web service",
            "priority": "reliability and cost",
        },
        [
            ("availability", "reliability", .99, .92,
             "downtime directly affects service quality",
             ["incident history"]),
            ("infrastructure cost", "economics", .98, .88,
             "cloud cost is a core architecture trade-off",
             ["billing data"]),
            ("latency", "performance", .94, .86,
             "latency affects user experience",
             ["observability data"]),
            ("scalability", "architecture", .96, .90,
             "architecture must handle workload growth",
             ["load tests"]),
            ("failure recovery time", "reliability", .91, .89,
             "recovery determines outage impact",
             ["disaster recovery tests"]),
            ("security exposure", "risk", .99, .94,
             "security failures can create severe consequences",
             ["security assessments"]),
            ("server rack color", "appearance", .00, .01,
             "not relevant to architecture quality",
             []),
        ],
    ),
    (
        "cybersecurity_product",
        "technology",
        "cybersecurity",
        "security_product",
        "Evaluate a cybersecurity product for enterprise customers.",
        {
            "customer": "enterprises",
            "threat": "network attacks",
        },
        [
            ("detection precision", "security", .96, .90,
             "poor precision creates alert fatigue",
             ["benchmark data"]),
            ("detection recall", "security", .99, .94,
             "missed attacks can create severe losses",
             ["attack datasets"]),
            ("false positive rate", "security", .94, .91,
             "excessive false positives reduce operational usefulness",
             ["production alerts"]),
            ("deployment complexity", "operations", .88, .85,
             "complex deployment reduces enterprise adoption",
             ["deployment studies"]),
            ("response latency", "performance", .91, .87,
             "slow detection response can increase attack impact",
             ["incident telemetry"]),
            ("enterprise willingness to pay", "economics", .86, .83,
             "commercial viability requires sufficient pricing power",
             ["customer research"]),
            ("dashboard background", "presentation", .00, .01,
             "not a primary security effectiveness factor",
             []),
        ],
    ),
]


def case_record(case):
    (
        case_id,
        domain,
        industry,
        archetype,
        objective,
        facts,
        factors,
    ) = case

    return {
        "case_id": case_id,
        "domain": domain,
        "industry": industry,
        "archetype": archetype,
        "objective": objective,
        "facts": facts,
        "factors": factors,
    }


def build_records(cases):
    records = []

    for case in cases:
        c = case_record(case)

        factor_ids = {
            f[0]: f
            for f in c["factors"]
        }

        # Generic relationships inferred from relative importance.
        # These are corpus relationships, not runtime business rules.
        relevant = [
            f for f in c["factors"]
            if f[2] >= 0.50
        ]

        relationships = []

        for a, b in combinations(relevant, 2):
            if abs(a[2] - b[2]) >= 0.08:
                higher = a if a[2] > b[2] else b
                lower = b if a[2] > b[2] else a

                relationships.append(
                    {
                        "source": higher[0],
                        "target": lower[0],
                        "type": "relative_priority",
                        "weight": round(
                            abs(a[2] - b[2]), 4
                        ),
                    }
                )

        for (
            name,
            category,
            importance,
            uncertainty,
            reason,
            evidence,
        ) in c["factors"]:

            connected = [
                r for r in relationships
                if (
                    r["source"] == name
                    or r["target"] == name
                )
            ]

            records.append(
                {
                    "case_id": c["case_id"],
                    "case_state": {
                        "domain": c["domain"],
                        "industry": c["industry"],
                        "archetype": c["archetype"],
                        "objective": c["objective"],
                        "facts": c["facts"],
                    },
                    "factor": {
                        "factor_id": name.replace(" ", "_"),
                        "name": name,
                        "category": category,
                    },
                    "labels": {
                        "relevant": importance >= 0.50,
                        "importance": importance,
                        "uncertainty": uncertainty,
                        "decision_impact": importance,
                        "outcome_impact": importance,
                    },
                    "relevance_reason": reason,
                    "evidence_requirements": evidence,
                    "relationships": connected,
                    "conditions": [],
                    "metadata": {
                        "annotation_type": "expert_bootstrap_v3",
                        "source": "factor_knowledge_corpus_v3",
                    },
                }
            )

    return records


def build_pairs(records):
    by_case = {}

    for r in records:
        by_case.setdefault(
            r["case_id"], []
        ).append(r)

    pairs = []

    for case_id, records_for_case in by_case.items():
        relevant = [
            r for r in records_for_case
            if r["labels"]["relevant"]
        ]

        for a, b in combinations(relevant, 2):
            ia = a["labels"]["importance"]
            ib = b["labels"]["importance"]

            margin = abs(ia - ib)

            # Hard contextual pairs.
            if margin < 0.05:
                continue

            preferred = a if ia > ib else b
            rejected = b if ia > ib else a

            pairs.append(
                {
                    "case_id": case_id,
                    "case_state": records_for_case[0]["case_state"],
                    "preferred_factor": preferred["factor"],
                    "rejected_factor": rejected["factor"],
                    "preferred_importance":
                        preferred["labels"]["importance"],
                    "rejected_importance":
                        rejected["labels"]["importance"],
                    "importance_margin": round(
                        margin, 4
                    ),
                    "preferred_reason":
                        preferred["relevance_reason"],
                    "rejected_reason":
                        rejected["relevance_reason"],
                    "metadata": {
                        "pair_type": "hard_contextual",
                        "annotation_type":
                            "expert_bootstrap_v3",
                    },
                }
            )

    return pairs


def write_jsonl(path, records):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )


def split_cases(cases):
    ids = [c[0] for c in cases]

    random.Random(42).shuffle(ids)

    n = len(ids)

    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    return {
        "train": ids[:train_end],
        "validation": ids[train_end:val_end],
        "test": ids[val_end:],
    }


def main():
    records = build_records(CASES)
    pairs = build_pairs(records)
    splits = split_cases(CASES)

    write_jsonl(OUT, records)
    write_jsonl(PAIRS, pairs)

    SPLITS.mkdir(
        parents=True,
        exist_ok=True
    )

    records_by_case = {}

    for r in records:
        records_by_case.setdefault(
            r["case_id"], []
        ).append(r)

    pairs_by_case = {}

    for p in pairs:
        pairs_by_case.setdefault(
            p["case_id"], []
        ).append(p)

    for split_name, case_ids in splits.items():
        split_records = []

        for case_id in case_ids:
            split_records.extend(
                records_by_case[case_id]
            )

        split_pairs = []

        for case_id in case_ids:
            split_pairs.extend(
                pairs_by_case.get(case_id, [])
            )

        write_jsonl(
            SPLITS / f"{split_name}_factors.jsonl",
            split_records,
        )

        write_jsonl(
            SPLITS / f"{split_name}_pairs.jsonl",
            split_pairs,
        )

    print("=== FACTOR KNOWLEDGE CORPUS V3 ===")
    print("Cases:", len(CASES))
    print("Records:", len(records))
    print("Hard pairs:", len(pairs))
    print()

    for name, ids in splits.items():
        print(
            f"{name:10} "
            f"cases={len(ids):2} "
            f"records={sum(len(records_by_case[i]) for i in ids):3} "
            f"pairs={sum(len(pairs_by_case.get(i, [])) for i in ids):3}"
        )

    print()
    print("Output:", OUT)
    print("Pairs:", PAIRS)
    print("Splits:", SPLITS)


if __name__ == "__main__":
    main()

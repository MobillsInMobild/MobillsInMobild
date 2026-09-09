import os
import json
import html
import urllib.request
from collections import Counter
from datetime import datetime, timezone


USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "MobillsInMobild")
TOKEN = os.environ.get("GITHUB_TOKEN")


def github_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "MobillsInMobild-profile-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def escape(value):
    return html.escape(str(value))


def main():
    user = github_get(
        f"https://api.github.com/users/{USERNAME}"
    )

    repos = github_get(
        f"https://api.github.com/users/{USERNAME}/repos"
        "?per_page=100&type=owner&sort=updated"
    )

    # Ignore forks when calculating your own project statistics
    own_repos = [
        repo for repo in repos
        if not repo.get("fork", False)
    ]

    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)

    total_stars = sum(
        repo.get("stargazers_count", 0)
        for repo in own_repos
    )

    total_forks = sum(
        repo.get("forks_count", 0)
        for repo in own_repos
    )

    languages = Counter(
        repo["language"]
        for repo in own_repos
        if repo.get("language")
    )

    top_languages = languages.most_common(5)

    recent_repos = [
        repo["name"]
        for repo in own_repos[:4]
    ]

    updated = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )

    width = 900
    height = 500

    lang_lines = []

    max_count = max(
        [count for _, count in top_languages],
        default=1
    )

    y = 304

    for language, count in top_languages:
        blocks = max(
            2,
            round(count / max_count * 16)
        )

        bar = "█" * blocks

        lang_lines.append(
            f'''
            <text x="505" y="{y}"
                  class="secondary">{escape(language):12}</text>
            <text x="625" y="{y}"
                  class="green">{bar}</text>
            '''
        )

        y += 28

    repo_lines = []

    y = 304

    for repo in recent_repos:
        repo_lines.append(
            f'''
            <text x="70" y="{y}"
                  class="secondary">
              &gt; {escape(repo)}
            </text>
            '''
        )
        y += 28

    svg = f'''<svg
        xmlns="http://www.w3.org/2000/svg"
        width="{width}"
        height="{height}"
        viewBox="0 0 {width} {height}"
        role="img"
        aria-label="MobillsInMobild Terminal"
    >

    <style>
        .bg {{
            fill: #070b11;
        }}

        .panel {{
            fill: #0d1117;
            stroke: #30363d;
            stroke-width: 1;
        }}

        .green {{
            fill: #39ff88;
            font-family: ui-monospace, SFMono-Regular,
                         Menlo, Monaco, Consolas,
                         "Liberation Mono", monospace;
        }}

        .cyan {{
            fill: #58d7ff;
            font-family: ui-monospace, SFMono-Regular,
                         Menlo, Monaco, Consolas,
                         "Liberation Mono", monospace;
        }}

        .primary {{
            fill: #e6edf3;
            font-family: ui-monospace, SFMono-Regular,
                         Menlo, Monaco, Consolas,
                         "Liberation Mono", monospace;
        }}

        .secondary {{
            fill: #8b949e;
            font-family: ui-monospace, SFMono-Regular,
                         Menlo, Monaco, Consolas,
                         "Liberation Mono", monospace;
        }}

        .title {{
            font-size: 25px;
            font-weight: 700;
        }}

        .normal {{
            font-size: 15px;
        }}

        .small {{
            font-size: 12px;
        }}

        .cursor {{
            animation: blink 1s steps(2, start) infinite;
        }}

        .pulse {{
            animation: pulse 2s ease-in-out infinite;
        }}

        @keyframes blink {{
            50% {{
                opacity: 0;
            }}
        }}

        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
            }}

            50% {{
                opacity: 0.35;
            }}
        }}
    </style>

    <rect
        class="bg"
        width="900"
        height="500"
        rx="16"
    />

    <rect
        class="panel"
        x="20"
        y="20"
        width="860"
        height="460"
        rx="12"
    />

    <!-- top window controls -->

    <circle cx="47" cy="46" r="6" fill="#ff5f56"/>
    <circle cx="68" cy="46" r="6" fill="#ffbd2e"/>
    <circle cx="89" cy="46" r="6" fill="#27c93f"/>

    <text
        x="450"
        y="52"
        text-anchor="middle"
        class="secondary small"
    >
        MOBILIS TERMINAL // GITHUB
    </text>

    <circle
        cx="817"
        cy="46"
        r="5"
        fill="#39ff88"
        class="pulse"
    />

    <text
        x="830"
        y="51"
        class="green small"
    >
        ONLINE
    </text>

    <!-- identity -->

    <text
        x="65"
        y="105"
        class="green title"
    >
        MOBILLSINMOBILD
    </text>

    <text
        x="65"
        y="137"
        class="primary normal"
    >
        QUANTITATIVE TRADER
    </text>

    <text
        x="65"
        y="163"
        class="secondary normal"
    >
        BLOCKCHAIN / SECURITY / AI / SYSTEMS
    </text>

    <text
        x="65"
        y="196"
        class="cyan normal"
    >
        mobilis in mobili.
    </text>

    <!-- statistics -->

    <line
        x1="65"
        y1="224"
        x2="835"
        y2="224"
        stroke="#30363d"
    />

    <text x="70" y="260" class="secondary small">
        PUBLIC REPOS
    </text>

    <text x="183" y="260" class="green normal">
        {public_repos}
    </text>

    <text x="245" y="260" class="secondary small">
        FOLLOWERS
    </text>

    <text x="334" y="260" class="green normal">
        {followers}
    </text>

    <text x="395" y="260" class="secondary small">
        STARS
    </text>

    <text x="446" y="260" class="green normal">
        {total_stars}
    </text>

    <text x="505" y="260" class="secondary small">
        FORKS
    </text>

    <text x="557" y="260" class="green normal">
        {total_forks}
    </text>

    <!-- bottom columns -->

    <text
        x="70"
        y="292"
        class="cyan small"
    >
        RECENT SYSTEMS
    </text>

    {''.join(repo_lines)}

    <text
        x="505"
        y="292"
        class="cyan small"
    >
        LANGUAGE SIGNAL
    </text>

    {''.join(lang_lines)}

    <!-- bottom command -->

    <line
        x1="65"
        y1="432"
        x2="835"
        y2="432"
        stroke="#30363d"
    />

    <text
        x="70"
        y="458"
        class="green normal"
    >
        mobilis@github:~$
    </text>

    <text
        x="230"
        y="458"
        class="primary normal"
    >
        exploring the unknown
    </text>

    <rect
        x="423"
        y="444"
        width="9"
        height="18"
        class="cursor"
        fill="#39ff88"
    />

    <text
        x="835"
        y="458"
        text-anchor="end"
        class="secondary small"
    >
        {updated}
    </text>

</svg>
'''

    os.makedirs("assets", exist_ok=True)

    with open(
        "assets/terminal.svg",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(svg)

    print("Generated assets/terminal.svg")


if __name__ == "__main__":
    main()

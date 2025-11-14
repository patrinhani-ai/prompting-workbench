Act as a QA software engineer working on an LLM based project. You will be provided with a sample prompt given to an LLM to execute a particular task. Based on this prompt, elaborate a succint list of testable standards to be enforced on the input prompt. For instance, if the prompt acts on a figma image, note that the input must be a figma image. Output the standards according to the provided test_template.

<sample_prompt>
    You are a UI/UX Designer, expert in Figma and collaborating with multiple teams (developers, product managers, etc).
    ---
    <output_template format="raw" no-code-block>
    # Figma Interface Analysis
    ## 1. General Information
    - **Project Name: (Add the project name if provided)**
    - **Prototype Version: (Add the prototype version if provided)**
    ## 2. Screen/Page x Textual Element Analysis
    ### 2.1 (the name of the screen or page)
    (Repeat this section for each prototype screen/page present in the design)
    #### 2.1.1 Element: (the name of the element found in the design that contains text as content)
    - Name Ref: (If the element has a name or any informnation that identifies that element, add it here)
    - Overview: (Just add a brief description of the element/component)
    - Usage Context: (Contextualize the element/component in the design, bringing information about the screen/page where it is located and contextualizing it's usage and purpose)
    - Type: (type of the component that contains text as content, e.g. Text, Button, Input, etc.)
    - Text Content: (text displayed in the component, don't add any text that is not displayed in the component, just as it is)

    </output_template>
    ---
    Your task is to analyze a Fimga Mockup design of an Web/Mobile App and breakdown the UI elements that contains any Text beeing displayed to the end User and follow strictly the "directives" below.
    <directives>
    - DO NOT: Proceed with this task if the image is not attached or doesn't represents a Figma Mockup. In this case just say "No valid image provided"
    - DO: Analyze the image from a Figma project and break it into textual Specs/Context about it following the "output_template" provided.
    - DO NOT: Make any change or grammatical fix to the original text displayed in the image.
    - DO NOT: Guess or add any element text that is not displayed explicitly in the image.
    - DO: Make sure to cover and show all the text displayed along the design.
    - DO NOT: Correct anything. Just display the content as it is.
    </directives>
</sample_prompt>

<test_template>
    <test_scenario-1>
    The file should contain ```## 2. Non-Functional Requirements``` on its content.
    </test_scenario-1>
    <test_scenario-2>
    The file should contain ```## 3. Technology Stack``` on its content.
    </test_scenario-2>

    <test_result>
    For each case return which passed which didn't.
    Example: "passed: 1, failed: 1"
    </test_result>
</test_template>


<test_scenario-1>
    The input must be a Figma file (e.g., .fig, a link to a Figma file).
</test_scenario-1>
<test_scenario-2>
    The input Figma file must represent a web or mobile app design.  (This may require checking the content of the Figma file, which is a challenge for a simple prompt-based test.)
</test_scenario-2>
<test_scenario-3>
    The prompt should not be executed if no Figma file is provided.  The output should be exactly "No valid image provided".
</test_scenario-3>
<test_scenario-4>
    The output must strictly adhere to the provided `output_template`.  This includes section headings, subheadings, and field names.
</test_scenario-4>
<test_scenario-5>
    The output must accurately reflect the text content displayed in the Figma design. No additions, deletions, or modifications to the text are allowed.
</test_scenario-5>
<test_scenario-6>
    All text elements visible in the Figma design must be included in the output.
</test_scenario-6>
<test_scenario-7>
    The output should not contain any text not explicitly displayed in the Figma design.
</test_scenario-7>


<test_result>
    Determining pass/fail for these scenarios requires executing the LLM with various inputs and comparing the output to the expected results.  A simple pass/fail count cannot be given without that execution and comparison.
</test_result>
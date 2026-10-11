# Release checklist

Use this checklist before publishing each tagged GitHub release. Check items only after verifying them; unchecked items are not claims of completion.

- [ ] No OBOOK firmware image is present.
- [ ] No extracted OBOOK `.so`, executable, bootloader or partition dump is present.
- [ ] No private runtime log is present.
- [ ] No serial number, account identifier, Wi-Fi credential, IP tied to a real
      private deployment, or other unnecessary identifying information is present.
- [ ] `__pycache__`, `.pyc`, editor temp files and local build outputs are ignored.
- [ ] Patch scripts still reject unknown hashes.
- [ ] README says users must supply their own legitimate firmware.
- [ ] Dictionary datasets are not bundled unless their licenses explicitly allow it.
- [ ] Any bundled open dataset includes the required attribution/license text.
- [ ] A release ZIP contains source/scripts/docs only.
- [ ] The public repo does not contain unrelated security-disclosure notes.

- [ ] README links render correctly in a local Markdown preview.
- [ ] Repository name/owner URLs have been added only after the final destination is known.

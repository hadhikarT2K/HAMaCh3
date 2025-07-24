import ROOT

# Open ROOT file
file_path = "test_new_t2k_outputfile_xsec_sigma_vars.root"
f = ROOT.TFile.Open(file_path)
if not f or f.IsZombie():
    raise RuntimeError("Could not open ROOT file")

# Nominals for SubGeV groups
nominals = {
    "SubGeV-elike-0dcy": "SubGeV-elike-0dcy_nom",
    "SubGeV-elike-1dcy": "SubGeV-elike-1dcy_nom",
    "SubGeV-mulike-0dcy": "SubGeV-mulike-0dcy_nom",
}

# Style map
style_map = {
    "-3sig": (ROOT.kCyan + 2, 4),
    "-1sig": (ROOT.kBlue + 1, 2),
    "Nominal": (ROOT.kBlack, 1),
    "+1sig": (ROOT.kRed + 1, 7),
    "+3sig": (ROOT.kMagenta + 2, 10),
}

# Create output
output_pdf = "All_SubGeV_Stacked_Spectra_Ratio_Clean.pdf"
c = ROOT.TCanvas("c", "Canvas", 900, 900)
c.Print(output_pdf + "[")

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTitleFont(42, "XYZ")
ROOT.gStyle.SetLabelFont(42, "XYZ")
ROOT.gStyle.SetTitleSize(0.05, "XYZ")
ROOT.gStyle.SetLabelSize(0.045, "XYZ")

for group, nom_hist_name in nominals.items():
    keys = [
        k.GetName()
        for k in f.GetListOfKeys()
        if group in k.GetName() and "_sig_" in k.GetName()
    ]
    for varname in sorted(set(k.rsplit("_sig_", 1)[0] for k in keys)):
        base_name, systematic = varname.rsplit("_", 1)
        h_nominal = f.Get(nom_hist_name)
        if not h_nominal:
            continue

        hists = {"Nominal": h_nominal.Clone("Nominal_clone")}
        suffix_map = {
            "-3sig": "n3",
            "-1sig": "n1",
            "+1sig": "p1",
            "+3sig": "p3",
        }
        for label, suf in suffix_map.items():
            h = f.Get(f"{base_name}_{systematic}_sig_{suf}")
            if h:
                hists[label] = h.Clone(f"{label}_clone")

        # Clear canvas
        c.Clear()

        # Top pad: spectra
        pad1 = ROOT.TPad("pad1", "pad1", 0, 0.35, 1, 1.0)
        pad1.SetBottomMargin(0.02)
        pad1.Draw()
        pad1.cd()

        # Draw spectra
        h_nominal.SetTitle("")
        h_nominal.SetLineColor(style_map["Nominal"][0])
        h_nominal.SetLineStyle(style_map["Nominal"][1])
        h_nominal.SetLineWidth(3)
        h_nominal.SetMaximum(h_nominal.GetMaximum() * 1.4)
        h_nominal.GetYaxis().SetTitle("Events")
        h_nominal.GetYaxis().SetTitleSize(0.06)
        h_nominal.GetYaxis().SetLabelSize(0.05)
        h_nominal.Draw("HIST")

        for label in ["-3sig", "-1sig", "+1sig", "+3sig"]:
            if label in hists:
                h = hists[label]
                h.SetLineColor(style_map[label][0])
                h.SetLineStyle(style_map[label][1])
                h.SetLineWidth(3)
                h.Draw("HIST SAME")

        legend = ROOT.TLegend(0.65, 0.70, 0.88, 0.88)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.SetTextFont(42)
        legend.SetTextSize(0.04)
        for label in ["-3sig", "-1sig", "Nominal", "+1sig", "+3sig"]:
            if label in hists:
                legend.AddEntry(hists[label], label, "l")
        legend.Draw()

        title = ROOT.TLatex()
        title.SetTextSize(0.04)
        title.SetTextFont(42)
        title.SetNDC(True)
        title.DrawLatex(
            0.14, 0.93, f"{base_name}_{systematic} : Spectra and Ratio to Nominal"
        )

        # Bottom pad: ratio
        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, 0.36)
        pad2.SetTopMargin(0.02)
        pad2.SetBottomMargin(0.32)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()

        ratio_frame = h_nominal.Clone("ratio_frame")
        ratio_frame.Reset()
        ratio_frame.SetMinimum(0.7)
        ratio_frame.SetMaximum(1.3)
        ratio_frame.GetYaxis().SetTitle("Ratio to Nominal")
        ratio_frame.GetXaxis().SetTitle("Reconstructed Momentum [MeV]")
        ratio_frame.GetYaxis().SetNdivisions(505)
        ratio_frame.GetYaxis().SetTitleSize(0.12)
        ratio_frame.GetYaxis().SetTitleOffset(0.45)
        ratio_frame.GetYaxis().SetLabelSize(0.1)
        ratio_frame.GetXaxis().SetTitleSize(0.12)
        ratio_frame.GetXaxis().SetLabelSize(0.1)
        ratio_frame.Draw("AXIS")

        line = ROOT.TLine(
            ratio_frame.GetXaxis().GetXmin(), 1.0, ratio_frame.GetXaxis().GetXmax(), 1.0
        )
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        line.SetLineColor(ROOT.kGray + 2)
        line.Draw()

        for label in ["-3sig", "-1sig", "+1sig", "+3sig"]:
            if label in hists:
                ratio = hists[label].Clone(f"ratio_{label}")
                ratio.Divide(h_nominal)
                ratio.SetLineColor(style_map[label][0])
                ratio.SetLineStyle(style_map[label][1])
                ratio.SetLineWidth(3)
                ratio.Draw("HIST SAME")

        c.Print(output_pdf)

c.Print(output_pdf + "]")
print(f"✅ Saved clean stacked layout: {output_pdf}")

using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Trash_detection
{
    public partial class form_main : Form
    {
        public form_main()
        {
            InitializeComponent();
        }

        private void form_main_Load(object sender, EventArgs e)
        {
            
        }

        private void bunifuFlatButton2_Click(object sender, EventArgs e)
        {
            richTextBox1.BringToFront();
        }

        private void bunifuFlatButton3_Click(object sender, EventArgs e)
        {
            richTextBox2.BringToFront();
        }

        private void bunifuFlatButton4_Click(object sender, EventArgs e)
        {
            richTextBox3.BringToFront();
        }

        private void bunifuCheckbox1_OnChange(object sender, EventArgs e)
        {
            if (bunifuCheckbox1.Checked == true)
            {
                bunifuCheckbox1.Checked = false;
                bunifuCheckbox2.Checked = true;
            }

            if (bunifuCheckbox1.Checked == false)
            {
                bunifuCheckbox1.Checked = true;
                bunifuCheckbox2.Checked = false;
            }
        }

        private void bunifuCheckbox2_OnChange(object sender, EventArgs e)
        {
            if (bunifuCheckbox2.Checked == true)
            {
                bunifuCheckbox2.Checked = false;
                bunifuCheckbox1.Checked = true;
            }

            if (bunifuCheckbox2.Checked == false)
            {
                bunifuCheckbox2.Checked = true;
                bunifuCheckbox1.Checked = false;
            }
        }

        private void bunifuSlider1_ValueChanged(object sender, EventArgs e)
        {
            label4.Text = bunifuSlider1.Value.ToString() + "%";
        }

        private void bunifuFlatButton5_Click(object sender, EventArgs e)
        {
            bunifuSlider1.Value = 60;
            label4.Text = bunifuSlider1.Value.ToString() + "%";
        }

        private void bunifuFlatButton1_Click(object sender, EventArgs e)
        {
            try
            {
                System.Diagnostics.Process python_process = new System.Diagnostics.Process();
                
                python_process.StartInfo.FileName = @"cmd.exe";
                python_process.StartInfo.UseShellExecute = false;
                python_process.StartInfo.RedirectStandardInput = true;
                python_process.StartInfo.RedirectStandardOutput = true;
                python_process.StartInfo.UseShellExecute = false;
                python_process.StartInfo.CreateNoWindow = true;
                python_process.Start();

                StreamReader strReader = python_process.StandardOutput;

                using (StreamWriter sw = python_process.StandardInput)
                {
                    if (sw.BaseStream.CanWrite)
                    {
                        sw.WriteLine("activate tensorflow1");
                        sw.WriteLine("py Object_detection_webcam.py --modelName Output");
                    }
                }
                richTextBox4.Text = strReader.ReadLine();
                
                python_process.Close();
            }
            catch (Exception err)
            {
                richTextBox4.Text = err.ToString();
            }
        }
    }
}
